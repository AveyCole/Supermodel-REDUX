"""CoreMIDI transport for the same framed Redux Workbench requests."""
import ctypes as c
import fcntl
import os
from pathlib import Path
import queue
import struct
import time

from capture_next_screen import HEADER, encode

CALLBACK = c.CFUNCTYPE(None, c.c_void_p, c.c_size_t)
COMMANDS = {*range(1, 22), 0x30, 0x31, 0x32, 0x40, 0x41, 0x42, *range(0x50, 0x57),
            *range(0x60, 0x68), 0x6a, 0x6b}


def load_bridge():
    target = Path(__file__).resolve().parents[2] / 'runtime/redux-coremidi.dylib'
    library = c.CDLL(str(target))
    library.redux_midi_open.argtypes = [c.c_char_p, CALLBACK, c.POINTER(c.c_void_p)]
    library.redux_midi_open.restype = c.c_int32
    library.redux_midi_send.argtypes = [c.c_void_p, c.c_char_p, c.c_size_t]
    library.redux_midi_send.restype = c.c_int32
    library.redux_midi_close.argtypes = [c.c_void_p]
    library.redux_midi_close.restype = None
    return library


class Replies:
    def __init__(self):
        self.packet = bytearray()

    def read(self, chunk):
        for value in chunk:
            if value >= 0xf8:
                continue
            if value == 0xf0:
                self.packet[:] = b'\xf0'
            elif not self.packet:
                continue
            elif value == 0xf7:
                wire = bytes(self.packet)
                self.packet.clear()
                if not wire.startswith(HEADER):
                    continue
                body = bytearray()
                for at in range(len(HEADER), len(wire), 8):
                    group = wire[at:at+8]
                    if len(group) < 2:
                        break
                    body.extend(byte | ((group[0] >> (6-index) & 1) << 7)
                                for index, byte in enumerate(group[1:]))
                else:
                    if len(body) >= 5:
                        yield bytes(body)
            elif value >= 0x80 or len(self.packet) >= 65536:
                self.packet.clear()
            else:
                self.packet.append(value)


class NextUSB:
    transport = 'CoreMIDI'

    def __init__(self, name='Supermodel Next', transport=None):
        if transport not in (None, 'coremidi'):
            raise ValueError('Unknown MIDI transport')
        self.library = load_bridge()
        self.device = c.c_void_p()
        self.queue = queue.SimpleQueue()
        self.replies = Replies()
        self.sequence = 0
        self.last_request = time.monotonic()

        @CALLBACK
        def receive(pointer, length):
            self.queue.put(c.string_at(pointer, length))

        self.callback = receive
        self.lock = (Path(os.environ['REDUX_STATE']) / 'scratch' / 'midi.lock').open('a+b')
        try:
            fcntl.flock(self.lock.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            result = self.library.redux_midi_open(name.encode(), receive, c.byref(self.device))
        except BlockingIOError as error:
            self.close()
            raise RuntimeError('A Workbench MIDI session is already active.') from error
        except BaseException:
            self.close()
            raise
        if result:
            self.close()
        if result == -70001:
            raise RuntimeError(f'Connect the Cycles and look for {name!r} in Audio MIDI Setup.')
        if result == -70002:
            raise RuntimeError(f'More than one MIDI endpoint matches {name!r}. Connect one Cycles at a time.')
        if result:
            raise RuntimeError(f'CoreMIDI could not open the Cycles ({result}).')

    def close(self):
        if self.device:
            self.library.redux_midi_close(self.device)
            self.device = c.c_void_p()
        self.lock.close()

    def send(self, packet):
        result = self.library.redux_midi_send(self.device, packet, len(packet))
        if result:
            raise OSError(f'CoreMIDI could not send the MIDI packet ({result}).')

    def request(self, kind, payload=b'', timeout=10, *, minimum_gap=.05):
        if kind not in COMMANDS:
            raise ValueError('Unsupported command')
        pause = minimum_gap - (time.monotonic() - self.last_request)
        if pause > 0:
            time.sleep(pause)
        self.sequence = (self.sequence + 1) & 65535
        response = struct.pack('>HB', self.sequence, kind | 128)
        try:
            self.send(encode(struct.pack('>HHB', self.sequence, 0, kind) + payload))
            deadline = time.monotonic() + timeout
            while (remaining := deadline - time.monotonic()) > 0:
                try:
                    chunk = self.queue.get(timeout=remaining)
                except queue.Empty:
                    break
                for reply in self.replies.read(chunk):
                    if reply[2:5] == response:
                        return reply
            raise TimeoutError(f'No reply for RPC {kind:02x}; upload not confirmed')
        finally:
            self.last_request = time.monotonic()
