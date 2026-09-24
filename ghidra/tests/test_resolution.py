#!/usr/bin/env python3
"""Regression tests for the CTF's Ghidra resolution tooling.

Asserts golden invariants on `resolve_functions.resolve()` built from the real
ground truth.  Runs anywhere - no Ghidra required.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
GHIDRA = HERE.parent
sys.path.insert(0, str(GHIDRA))
import resolve_functions as rf  # noqa: E402


def main() -> int:
    """
    Run the tooling assertions.

    Parameters
    ----------
    None

    Returns
    -------
    int
        Zero when every check passes.
    """
    rows = rf.resolve()
    kinds: dict[str, int] = {}
    for r in rows:
        kinds[r["kind"]] = kinds.get(r["kind"], 0) + 1
    by_addr = {r["addr"]: r for r in rows}

    def named(addr: int) -> str:
        return by_addr[addr]["name"]

    checks = [
        ("total functions == 50", len(rows) == 50),
        ("application == 10", kinds.get("application") == 10),
        ("PLT0 detected", rf.find_plt0() > 0),
        ("0x400960 -> ctf_crc32_le", named(0x400960) == "ctf_crc32_le"),
        ("0x4009b0 -> ctf_weak_key", named(0x4009B0) == "ctf_weak_key"),
        ("0x400ae0 -> ctf_config_run", named(0x400AE0) == "ctf_config_run"),
        ("0x400bc0 -> ctf_restore", named(0x400BC0) == "ctf_restore"),
        ("B1..B6 present",
         all(any(v in r.get("brief", "") for r in rows)
             for v in ("B1", "B2", "B3", "B4", "B5", "B6"))),
    ]
    passed = sum(1 for _, p in checks if p)
    for name, good in checks:
        print(("PASS " if good else "FAIL ") + name)
    print(f"{passed}/{len(checks)} checks, {len(checks) - passed} failures")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
