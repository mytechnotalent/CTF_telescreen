# OPERATION TELESCREEN CTF - Design Blueprint

Artifact prefix: `CTF-XX`
Repo: `CTF_telescreen`
Companion project: `telescreen`
Author: Kevin Thomas (kevin@mytechnotalent.com)

This document is the build spine. It is not student-facing. Student-facing docs are
the canonical `CTF-XX-I.md`, `CTF-XX-R.md`, and `CTF-XX-S.md` plus their PDFs.

***

## What this CTF is

A Raspberry Pi 5 (Cortex-A76, Linux) surveillance camera/router whose firmware is four
partitions. The student receives the **compromised** image, carves it, reverses the
boot chain, finds six backdoors, breaks the weak exfiltration key, and rebuilds a
hardened image.

## Why this one is different

1. **Application-class, not bare-metal.** The target is Linux on a Cortex-A; the
   student meets a real U-Boot -> kernel -> JFFS2 chain, not a single `.bin`.
2. **The four-partition model.** The student proves the layout from bytes and uses real
   tooling (`dd`, `binwalk`, `objdump`, `jefferson`, `mkfs.jffs2`).
3. **A real cryptographic fix.** Students break a key derived from a public UID and
   replace it with X25519 + HKDF + AES-256-GCM.
4. **Both sides of the story.** The companion project builds the defended device; this
   CTF hands them the compromised one.

## Artifact construction (with the tools)

```bash
# build the four images from the lab tree
python3 scripts/build_images.py --uboot boot.bin --kernel Image --rootfs rootfs/ --out out/
# carve and verify the whole image
python3 scripts/verify_telescreen.py --image CTF-XX-full.img
# the hardened reference
cp CTF-XX-full.img CTF-XX-full_fixed.img   # then apply the hardening patches
```

## Defect map

| # | defect | partition | fix |
|---|--------|-----------|-----|
| B1 | config-sourced root exec | rootfs | validate / stop sourcing config as root |
| B2 | CGI command injection | kernel/app | use `execve` with an argument vector |
| B3 | archive-to-root restore | kernel/app | reject `../` entries; drop privileges |
| B4 | empty / default credentials | rootfs | set a real password; require auth |
| B5 | debug root shell | rootfs | remove the debug path |
| B6 | weak key schedule | kernel/app | X25519 + HKDF + AES-256-GCM |

## Grading

See `CTF-XX-R.md`. Each defect is provable on a Raspberry Pi 5 with the four images
and a serial console.
