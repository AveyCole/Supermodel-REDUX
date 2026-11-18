"""Run the portable Workbench from a macOS application bundle."""
import fcntl
import json
import os
from pathlib import Path
import secrets
import subprocess
import sys
import time
from urllib.request import ProxyHandler, build_opener

ROOT = Path(__file__).resolve().parent
VERSION = (ROOT / 'revision.txt').read_text().strip()
STATE = Path(os.environ.get('REDUX_STATE', Path.home() / 'Library/Application Support/Supermodel REDUX' / VERSION))
SCRATCH = STATE / 'scratch'
READY = SCRATCH / 'workbench-ready.txt'
REFERENCE = STATE / 'reference/model-cycles_OS1.13.syx'
TOOLS = ROOT / 'next-os/tools'


def configure():
    SCRATCH.mkdir(parents=True, exist_ok=True)
    REFERENCE.parent.mkdir(exist_ok=True)
    path = os.environ.get('PATH', '/usr/bin:/bin:/usr/sbin:/sbin')
    cross = os.environ.get('SM_M68K_CROSS', str(ROOT / 'runtime/toolchain/bin/m68k-elf-'))
    if not Path(cross + 'gcc').is_file():
        raise RuntimeError('The Workbench app is incomplete. Extract the entire ZIP and reopen the app.')
    cross_bin = str(Path(cross).parent)
    os.environ.update(REDUX_PORTABLE='1', REDUX_REVISION=VERSION, REDUX_STATE=str(STATE),
                      REDUX_REFERENCE=str(REFERENCE), SM_M68K_CROSS=cross,
                      TEMP=str(SCRATCH), TMP=str(SCRATCH), TMPDIR=str(SCRATCH),
                      PATH=cross_bin + os.pathsep + path)
    sys.path.insert(0, str(TOOLS))


def server_url():
    try:
        port, token = READY.read_text(encoding='ascii').splitlines()
        port = int(port)
        if not 1 <= port <= 65535:
            return None
        url = f'http://127.0.0.1:{port}'
        opener = build_opener(ProxyHandler({}))
        with opener.open(url + '/api/workbench-session', timeout=.5) as reply:
            if json.load(reply) == {'version': VERSION, 'session': token}:
                return url + '/'
    except (OSError, ValueError):
        return None


def launch(open_browser):
    url = server_url()
    if not url:
        with (SCRATCH / 'workbench.log').open('ab') as log:
            subprocess.Popen([sys.executable, '-B', '-u', __file__, '--serve'],
                             stdout=log, stderr=log, stdin=subprocess.DEVNULL, start_new_session=True)
        deadline = time.monotonic() + 15
        while not url and time.monotonic() < deadline:
            time.sleep(.15)
            url = server_url()
    if not url:
        raise RuntimeError('The local Workbench could not start. See ' + str(SCRATCH / 'workbench.log'))
    if open_browser:
        subprocess.run(['/usr/bin/open', url], check=True)
    else:
        print(url)


def run():
    configure()
    mode = sys.argv[1] if len(sys.argv) > 1 else '--launch'
    if mode in ('--launch', '--launch-url'):
        launch(mode == '--launch')
        return
    if mode == '--import-reference':
        from package_owned_main import OFFICIAL_SHA
        import hashlib
        raw = Path(sys.argv[2]).read_bytes()
        if hashlib.sha256(raw).hexdigest() != OFFICIAL_SHA:
            raise ValueError('Choose the official Model:Cycles OS 1.13 SysEx, inside the Elektron download.')
        pending = REFERENCE.with_suffix('.tmp')
        pending.write_bytes(raw)
        pending.replace(REFERENCE)
        return
    with (SCRATCH / 'workbench.lock').open('a+b') as lock:
        try:
            fcntl.flock(lock.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            raise SystemExit('Workbench is already running.')
        import flasher_server_lead431 as server
        server.JOBS = STATE / 'jobs'
        READY.unlink(missing_ok=True)
        os.environ.update(REDUX_LAUNCH_SESSION=secrets.token_hex(24), REDUX_LAUNCH_READY=str(READY))
        sys.argv = [sys.argv[0], '--port', '0']
        server.main()


if __name__ == '__main__':
    run()
