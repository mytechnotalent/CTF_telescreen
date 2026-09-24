#!/usr/bin/env python3
"""Regression test: the compiled CTF node and the Python tool must agree.

This guards the weak key schedule (defect B6) against drift.  The stripped
aarch64 binary's `key <uid>` output must equal ``weak_decrypt.weak_key(uid)``
and both must equal the published vector.  (It catches exactly the failure we
hit: a standard CRC-32 with a final XOR vs the JFFS2-style crc32_le.)

The binary is run natively on aarch64 Linux, otherwise inside the pinned
``telescreen-cross:arm64`` Docker image (macOS / Windows / x86).
"""
import platform
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BIN = ROOT / "firmware" / "ctfnode.stripped"
DOCKER_IMAGE = "telescreen-cross:arm64"

sys.path.insert(0, str(HERE))
import weak_decrypt  # noqa: E402

UID = "SSAT-468547-FEEBD"
EXPECTED = "da506e04af00c6f40394d2cd2295bfc8682e8b9f9e9b844cea50c08d5f483141"


def binary_key(uid: str) -> str:
    """
    Return the key the compiled node prints for a UID.

    Parameters
    ----------
    uid : str
        Public device identifier.

    Returns
    -------
    str
        Lowercase hex key the binary produced.
    """
    if not BIN.exists():
        print("FAIL firmware/ctfnode.stripped missing - run ./firmware/build_target.sh")
        raise SystemExit(2)
    if platform.system() == "Linux" and platform.machine() == "aarch64":
        out = subprocess.check_output([str(BIN), "key", uid], text=True)
    else:
        cmd = ["docker", "run", "--rm", "--platform", "linux/arm64",
               "-v", f"{BIN.parent}:/fw", "-w", "/fw", DOCKER_IMAGE,
               "./ctfnode.stripped", "key", uid]
        out = subprocess.check_output(cmd, text=True)
    return out.strip()


def main() -> int:
    """
    Run the consistency checks.

    Parameters
    ----------
    None

    Returns
    -------
    int
        Zero when every check passes.
    """
    py_key = weak_decrypt.weak_key(UID).hex()
    c_key = binary_key(UID)
    checks = (
        ("python tool == published vector", py_key == EXPECTED),
        ("stripped binary == published vector", c_key == EXPECTED),
        ("python tool == stripped binary", py_key == c_key),
    )
    ok = True
    for name, passed in checks:
        print(("PASS " if passed else "FAIL ") + name)
        ok = ok and passed
    print("python:", py_key)
    print("binary:", c_key)
    print(f"{sum(1 for _, p in checks if p)}/{len(checks)} checks, "
          f"{0 if ok else 1} failures")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
