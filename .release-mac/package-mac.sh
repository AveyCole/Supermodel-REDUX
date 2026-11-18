#!/bin/bash
set -euo pipefail
arch="$1"
label="$2"
root="$RUNNER_TEMP/workbench package"
mkdir -p "$root" dist
/usr/bin/ditto -x -k "$RUNNER_TEMP/Supermodel-Redux-Mac-V942.zip" "$root"
folder="$root/Redux-Mac-V942"
app="$folder/Supermodel REDUX Workbench.app"
resources="$app/Contents/Resources"
runtime="$resources/runtime"
mkdir "$runtime"
case "$arch" in
  aarch64) sha=2f11b8aa3726bdbd87dd9eb76568412faddf4f47e26913fa45d6a2e424972acd ;;
  x86_64) sha=b78a4c479f1964ec484880bee567568266f68da102269fb93a05fe8716b45f91 ;;
  *) exit 2 ;;
esac
archive="cpython-3.12.16%2B20261110-$arch-apple-darwin-install_only_stripped.tar.gz"
/usr/bin/curl -fsSL --retry 3 "https://github.com/astral-sh/python-build-standalone/releases/download/20261110/$archive" -o "$RUNNER_TEMP/redux-python.tar.gz"
printf '%s  %s\n' "$sha" "$RUNNER_TEMP/redux-python.tar.gz" | shasum -a 256 -c -
/usr/bin/tar -xzf "$RUNNER_TEMP/redux-python.tar.gz" -C "$runtime"
env HOMEBREW_NO_AUTO_UPDATE=1 HOMEBREW_NO_INSTALL_CLEANUP=1 brew install m68k-elf-gcc
python3 .release-mac/bundle-mac-runtime.py "$runtime/toolchain"
# Compiler headers and notices remain in the toolchain alongside the binaries.
for formula in m68k-elf-gcc m68k-elf-binutils; do
  brew info --json=v2 "$formula" > "$runtime/toolchain/$formula.json"
done
/usr/bin/xcrun clang -mmacosx-version-min=12.0 -O2 -dynamiclib -framework CoreMIDI \
  -framework CoreFoundation "$resources/next-os/tools/macos_coremidi.c" -o "$runtime/redux-coremidi.dylib"
cp .release-mac/Workbench "$app/Contents/MacOS/Workbench"
chmod 755 "$app/Contents/MacOS/Workbench"
cp .release-mac/macos_next_usb.py "$resources/next-os/tools/next_usb.py"
cp .release-mac/macos_workbench_entry.py "$resources/macos_workbench_entry.py"
cp .release-mac/Manual.md "$folder/Manual.md"
cp .release-mac/Manual.md "$resources/next-os/flasher-prototype/dist-431/Supermodel-REDUX-Manual.md"
cp '.release-mac/Start Here.txt' "$folder/Start Here.txt"

# Sign and test after relocation, with a minimal user environment.
# Homebrew bottles on macos-15 may depend on system libraries from macOS 15.
/usr/libexec/PlistBuddy -c 'Set LSMinimumSystemVersion 15.0' "$app/Contents/Info.plist"
/usr/bin/codesign --force --deep --sign - "$app"
/usr/bin/codesign --verify --deep --strict "$app"
output="$PWD/dist/Supermodel-Redux-Mac-V942-$label.zip"
/usr/bin/ditto -c -k --keepParent "$folder" "$output"
check="$RUNNER_TEMP/relocated app check"
mkdir -p "$check"
/usr/bin/ditto -x -k "$output" "$check"
resources="$check/Redux-Mac-V942/Supermodel REDUX Workbench.app/Contents/Resources"
runtime="$resources/runtime"
# Remove the original bundle so fixtures cannot resolve to the build location.
mv "$folder" "$RUNNER_TEMP/original-package"
# Hide the installed cross-toolchain from the relocatability check. The
# Homebrew formula compiled in absolute fallback paths to its assembler and linker.
for formula in m68k-elf-gcc m68k-elf-binutils; do
  keg="$(cd "$(brew --prefix "$formula")" && pwd -P)"
  mv "$keg" "$RUNNER_TEMP/$formula-keg"
done
env -i HOME="$HOME" PATH=/usr/bin:/bin:/usr/sbin:/sbin REDUX_STATE="$check/user state" \
  SM_M68K_CROSS="$runtime/toolchain/bin/m68k-elf-" PYTHONNOUSERSITE=1 \
  "$runtime/python/bin/python3" -B .release-mac/smoke-mac-runtime.py "$resources" "$check/test build"
