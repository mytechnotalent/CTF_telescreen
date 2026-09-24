#!/usr/bin/env bash
#
# build_target.sh - build the TELESCREEN CTF node (the vulnerable target).
#
# This is the CTF counterpart of the lab's firmware/build_target.sh.  It
# compiles ctf/ctfnode.c - the deliberately vulnerable node that contains the
# six defects B1-B6 - into a stripped Linux aarch64 binary and an unstripped
# answer key.
#
#   ctfnode.unstripped  - names present (instructor answer key)
#   ctfnode.stripped    - names removed (the student target)
#
# The build runs in a pinned linux/arm64 container, so the output is identical
# on Windows x64, Linux x64, and macOS arm64.  See the lab's
# docs/31-prerequisites-and-install.md for install instructions.
#
# HOW TO RUN:
#
#   ./firmware/build_target.sh
#
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$HERE/.." && pwd)"
SRC="$ROOT/ctf"
DOCKER_IMAGE="telescreen-cross:arm64"
DOCKERFILE_DIR="$HERE/.docker"
PLATFORM="${PLATFORM:-linux/arm64}"

echo "[*] Repository root : $ROOT"
echo "[*] Source          : $SRC/ctfnode.c"

if ! command -v docker >/dev/null 2>&1; then
    echo "[!] Docker is not installed or not on your PATH."
    exit 1
fi

mkdir -p "$DOCKERFILE_DIR"
cat > "$DOCKERFILE_DIR/Dockerfile" <<'DOCKERFILE'
FROM gcc:14
DOCKERFILE
echo "[*] Ensuring toolchain image exists: $DOCKER_IMAGE"
docker build -q -t "$DOCKER_IMAGE" "$DOCKERFILE_DIR" >/dev/null

echo "[*] Compiling CTF node -> ctfnode.stripped"
docker run --rm --platform "$PLATFORM" \
    -v "$ROOT":/repo \
    -w /repo/firmware \
    "$DOCKER_IMAGE" bash -lc '
        set -e
        gcc -O2 -Wall -Wextra -o ctfnode.unstripped /repo/ctf/ctfnode.c
        cp ctfnode.unstripped ctfnode.stripped
        strip --strip-all ctfnode.stripped
        echo "    unstripped: $(stat -c %s ctfnode.unstripped) bytes"
        echo "    stripped  : $(stat -c %s ctfnode.stripped) bytes"
    '

echo
echo "[*] SHA-256:"
( cd "$HERE" && shasum -a 256 ctfnode.unstripped ctfnode.stripped )

# --- Ground truth for the Ghidra resolution pipeline ------------------------
GT_DIR="$ROOT/ghidra/ground_truth"
if [ -d "$ROOT/ghidra" ]; then
    mkdir -p "$GT_DIR"
    echo "[*] Capturing ground truth (nm/readelf/objdump) -> ghidra/ground_truth"
    docker run --rm --platform "$PLATFORM" \
        -v "$HERE":/fw -v "$GT_DIR":/gt -w /fw "$DOCKER_IMAGE" bash -lc '
            nm --defined-only ctfnode.unstripped | sort > /gt/symbols.txt
            readelf -rW ctfnode.stripped | awk "/JUMP_SLOT/ {print \$5}" | sort -u > /gt/imports.txt
            readelf -h ctfnode.stripped > /gt/elf_header.txt
            readelf -SW ctfnode.stripped > /gt/sections.txt
            readelf -rW ctfnode.stripped > /gt/relocs.txt
            objdump -d ctfnode.unstripped > /gt/disasm.txt
        '
fi

echo
echo "[*] Proving the stripped node runs natively (aarch64 Linux in Docker):"
docker run --rm --platform "$PLATFORM" \
    -v "$HERE":/fw -w /fw "$DOCKER_IMAGE" \
    bash -lc './ctfnode.stripped key SSAT-468547-FEEBD; echo "    exit code = $?"'
