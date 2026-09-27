# OPERATION TELESCREEN CTF - Design Blueprint

Artifact prefix: `CTF-XX`
Repo: `CTF_telescreen`
Companion project: `telescreen`
Author: Kevin Thomas (kevin@mytechnotalent.com)

This document is the build spine. It is not student-facing. Student-facing docs are
the canonical `CTF-XX-I.md`, `CTF-XX-R.md`, and `CTF-XX-S.md` plus their PDFs.

***

## What this CTF is

The captured TELESCREEN node is a **daemon** - a Linux aarch64 application that runs
as root on the device. The flash did not survive capture, so the **only** artifact is
the application binary, shipped **stripped** with no names and no source. The student
reverses it, recovers the command surface, names every function, proves the six
deliberate defects (B1-B6), breaks the weak exfiltration key, and writes a hardened
replacement.

There is **no boot chain** in this challenge. There is no U-Boot, no environment
partition, no kernel container, no device tree, and no JFFS2. Do not look for them;
they are not part of the artifact.

## Why this one is different

1. **Application-class, not bare-metal.** The target is an ELF on a Cortex-A SoC; the
   student meets real dynamic linking, `.plt`/`.got` indirection, and a stripped
   symbol table.
2. **Pure static RE with live proof.** Every defect is located in the machine code and
   then demonstrated by running the same binary inside a pinned container
   (`scripts/test_defects.py`), with no hardware and no network.
3. **A real cryptographic fix.** Students break a key derived from a public UID and
   replace it with X25519 + HKDF + AES-256-GCM.
4. **Both sides of the story.** The companion project builds the defended device; this
   CTF hands them the compromised daemon.

## Artifact construction

The single surviving artifact is built from source in a pinned `linux/arm64`
container so the bytes are identical on Windows x64, Linux x64, and macOS arm64:

```bash
./firmware/build_target.sh
# gcc:14, -O2 -Wall -Wextra
#   ctfnode.unstripped  (with names - answer key)
#   ctfnode.stripped    (strip --strip-all - student target)
```

`build_target.sh` also captures `nm`/`readelf`/`objdump` ground truth into
`ghidra/ground_truth/` and runs the stripped node natively in the container as a
smoke test.

Artifact identity:

```text
ctfnode.stripped   af7ab5c2b4837083682db8b54f6892b1a2a33dcc8ce7b202b5a4a5163232da6d
ctfnode.unstripped 6bcee7daa91280eaf02558b1b5f1b5cc8e22a84179605a0725af2b5564257e0a
```

## The resolution pipeline

`ghidra/make_project.sh` imports and auto-analyses `ctfnode.stripped` into
`ghidra/proj/CTFNodeRE.gpr`. `ghidra/resolve_functions.py` then produces
`ghidra/RESOLUTION_MAP.md`, `ghidra/resolution.json`, and `ghidra/resolved/` from the
ground truth plus the decompilation, and `ghidra/gen_appendix_j.py` produces
`CTF-XX-J-ghidra-function-resolution.md`. Those four outputs are the source of truth
for function addresses and names.

## Defect map

| # | defect | function | address | fix |
|---|--------|----------|---------|-----|
| B1 | config-sourced root exec | `ctf_config_run` | `0x400ae0` | parse a fixed schema; never `system()` a config line |
| B2 | command injection | `ctf_http_handle` / `ctf_build_cmd` | `0x400b80` / `0x400b64` | use `execve` with an argument vector |
| B3 | archive-to-root restore | `ctf_restore` | `0x400bc0` | reject `../` entries; stage, then drop privileges |
| B4 | empty / default credentials | `ctf_login` | `0x400a8c` | set a real password; require auth |
| B5 | debug root shell | `ctf_debug_shell` | `0x400c00` | remove the debug path from production |
| B6 | weak key schedule | `ctf_weak_key` | `0x4009b0` | X25519 + HKDF + AES-256-GCM |

All defects are **local** file/argument-to-root-execution flaws in the node's own
command surface; there is no network listener in the binary.

## Grading

See `CTF-XX-R.md`. Each defect is provable statically from the stripped binary and
dynamically with the containerized harnesses.
