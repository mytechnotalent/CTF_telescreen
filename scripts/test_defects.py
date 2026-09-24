#!/usr/bin/env python3
"""Live defect harness: prove B1-B6 actually manifest in the compiled node.

Runs the stripped aarch64 binary with crafted inputs inside the pinned
``telescreen-cross:arm64`` container (or natively on aarch64 Linux) and asserts
each defect's effect.  No hardware and no network required.

    B1  config-sourced root exec      -> a `run=` line triggers a command
    B2  CGI command injection         -> `; touch` runs as root
    B3  archive-to-root restore       -> a tar entry lands in /
    B4  default credentials           -> admin/"" is accepted, a wrong one is not
    B5  debug root shell              -> `/bin/sh` executes input
    B6  weak key schedule             -> covered by test_consistency.py
"""
import platform
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BIN = ROOT / "firmware" / "ctfnode.stripped"
IMAGE = "telescreen-cross:arm64"

SCRIPT = r"""
set -u
BIN=./ctfnode.stripped
[ -x "$BIN" ] || { echo "FAIL target missing"; exit 2; }
fail=0
chk() { if [ "$1" = ok ]; then echo "PASS $2"; else echo "FAIL $2"; fail=$((fail+1)); fi; }

printf 'run=touch /tmp/d1\n' > /tmp/cfg
rm -f /tmp/d1; $BIN config /tmp/cfg >/dev/null 2>&1
[ -f /tmp/d1 ] && r=ok || r=no; chk $r "B1 config-sourced root exec"

rm -f /tmp/d2; $BIN http '127.0.0.1; touch /tmp/d2' >/dev/null 2>&1
[ -f /tmp/d2 ] && r=ok || r=no; chk $r "B2 CGI command injection"

mkdir -p /tmp/src/tmp; echo hi > /tmp/src/tmp/d3
( cd /tmp/src && tar czf /tmp/u.tgz tmp/d3 )
rm -f /tmp/d3; $BIN restore /tmp/u.tgz >/dev/null 2>&1
[ -f /tmp/d3 ] && r=ok || r=no; chk $r "B3 archive-to-root restore"

$BIN login admin '' >/dev/null 2>&1 && r=ok || r=no; chk $r "B4 default credentials accepted"
$BIN login admin wrongpw >/dev/null 2>&1 && r=no || r=ok; chk $r "B4 wrong password rejected"

out=$(echo 'echo d5' | $BIN shell 2>/dev/null)
echo "$out" | grep -q d5 && r=ok || r=no; chk $r "B5 debug root shell"

echo "FAILURES=$fail"
exit $fail
"""


def main() -> int:
    """
    Run the defect harness and forward its output.

    Parameters
    ----------
    None

    Returns
    -------
    int
        Zero when every defect manifests.
    """
    if not BIN.exists():
        print("FAIL firmware/ctfnode.stripped missing - run ./firmware/build_target.sh")
        return 2
    if platform.system() == "Linux" and platform.machine() == "aarch64":
        res = subprocess.run(["bash", "-lc", SCRIPT], cwd=BIN.parent,
                             text=True, capture_output=True)
    else:
        cmd = ["docker", "run", "--rm", "--platform", "linux/arm64",
               "-v", f"{BIN.parent}:/fw", "-w", "/fw", IMAGE,
               "bash", "-lc", SCRIPT]
        res = subprocess.run(cmd, text=True, capture_output=True)
    sys.stdout.write(res.stdout)
    if res.stderr:
        sys.stderr.write(res.stderr)
    return res.returncode


if __name__ == "__main__":
    raise SystemExit(main())
