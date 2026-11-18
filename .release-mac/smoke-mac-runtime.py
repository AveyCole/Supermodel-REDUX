"""Check the relocated runtime, CoreMIDI, and the V942 compile and link path."""
import json
import os
from pathlib import Path
import subprocess
import sys
from urllib.request import urlopen

import audioop
import fcntl

resources, work = map(Path, sys.argv[1:])
tools = resources / 'next-os/tools'
sys.path.insert(0, str(tools))
from macos_next_usb import load_bridge
from build_flasher_profile import compile_objects, link_firmware, parse, run

load_bridge()
os.environ['COMPILER_PATH'] = str(resources / 'runtime/toolchain/m68k-elf/bin')
config = dict(schema='supermodel-next-config/v2', target='model-cycles', core='required',
              state='selection-not-compiled', machines=['stock-metal', 'stock-kick', 'sample-wizard'],
              effects=['delay', 'reverb'], features=['stock-mask', 'usb6', 'master-retrig'])
selected = parse(json.dumps(config), 'V942')
work.mkdir()
linked = link_firmware(work, compile_objects(work, selected, {}, None))
if linked.returncode:
    raise RuntimeError(linked.stderr.decode(errors='replace'))
assert (work / 'firmware.elf').read_bytes().startswith(b'\x7fELF')
assert b'MC68000' in run('readelf', '-h', work / 'firmware.elf')
url = subprocess.check_output([sys.executable, '-B', resources / 'macos_workbench_entry.py',
                               '--launch-url'], text=True).strip()
with urlopen(url, timeout=5) as response:
    assert response.status == 200
    assert b'Workbench' in response.read()
print('Bundled Python, CoreMIDI, ColdFire build/link, and Workbench startup passed.')
