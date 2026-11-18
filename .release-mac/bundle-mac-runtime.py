"""Relocate the Homebrew ColdFire cross-compiler into the Workbench app."""
import os
from pathlib import Path
import shutil
import subprocess
import sys

toolchain = Path(sys.argv[1]).resolve()
toolchain.mkdir(parents=True, exist_ok=True)
libraries = toolchain / 'runtime-libs'
libraries.mkdir()
sources = {}
mach_magics = {bytes.fromhex(value) for value in (
    'feedface', 'feedfacf', 'cefaedfe', 'cffaedfe', 'cafebabe', 'bebafeca', 'cafebabf', 'bfbafeca'
)}


def run(command, *args):
    return subprocess.check_output([command, *map(str, args)], text=True)


def is_macho(path):
    with path.open('rb') as stream:
        return stream.read(4) in mach_magics


def system_path(name):
    return name.startswith(('/usr/lib/', '/System/Library/'))


def dependencies(path):
    return {line.strip().split(' (compatibility version', 1)[0]
            for line in run('/usr/bin/otool', '-L', path).splitlines()
            if ' (compatibility version' in line}


def resolve_dependency(name, source):
    if name.startswith('/'):
        return Path(name).resolve(strict=True)
    if name.startswith(('@executable_path/', '@loader_path/')):
        return (source.parent / name.split('/', 1)[1]).resolve(strict=True)
    if name.startswith('@rpath/'):
        for line in run('/usr/bin/otool', '-l', source).splitlines():
            if line.strip().startswith('path ') and ' (offset ' in line:
                entry = line.strip()[5:].split(' (offset ', 1)[0]
                root = Path(entry.replace('@loader_path', str(source.parent))
                                 .replace('@executable_path', str(source.parent)))
                candidate = root / name.removeprefix('@rpath/')
                if candidate.is_file():
                    return candidate.resolve()
    raise RuntimeError(f'Unable to locate {name} needed by {source}')


for formula in ('m68k-elf-binutils', 'm68k-elf-gcc'):
    keg = Path(run('brew', '--prefix', formula).strip()).resolve(strict=True)
    shutil.copytree(keg, toolchain, dirs_exist_ok=True, ignore_dangling_symlinks=True)
    for source in keg.rglob('*'):
        target = toolchain / source.relative_to(keg)
        if target.is_file() and is_macho(target):
            sources[target] = source.resolve(strict=True)

pending = list(sources)
while pending:
    binary = pending.pop()
    source = sources[binary]
    original = dependencies(binary)
    install_ids = {line.strip() for line in run('/usr/bin/otool', '-D', binary).splitlines()
                   if line.strip() in original and not line.strip().endswith(':')}
    changes = []
    for name in sorted(original - install_ids):
        if system_path(name):
            continue
        dependency = resolve_dependency(name, source)
        if system_path(str(dependency)):
            changes.extend(('-change', name, str(dependency)))
            continue
        target = libraries / dependency.name
        if target not in sources:
            shutil.copy2(dependency, target)
            sources[target] = dependency
            pending.append(target)
        elif sources[target] != dependency:
            raise RuntimeError(f'Duplicate runtime library name {dependency.name}')
        changes.extend(('-change', name, '@loader_path/' + os.path.relpath(target, binary.parent)))
    if install_ids:
        changes.extend(('-id', '@rpath/' + binary.name))
    if changes:
        binary.chmod(binary.stat().st_mode | 0o200)
        run('/usr/bin/install_name_tool', *changes, binary)
    run('/usr/bin/codesign', '--force', '--sign', '-', binary)
