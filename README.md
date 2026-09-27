![CTF // TELESCREEN](CTF_telescreen.png)

<br>

## FREE Reverse Engineering Self-Study Course [HERE](https://github.com/mytechnotalent/reverse-engineering)
## FREE Embedded Hacking Course [HERE](https://github.com/mytechnotalent/Embedded-Hacking)

<br>

# OPERATION TELESCREEN CTF

### The Compromised Surveillance Node
#### The finale after OPERATION COLD IRON

Capture the Flag XX - **The compromised surveillance node**

<br>

***
**LEGAL DISCLAIMER:**
The information, tools, and code provided in this repository and course are strictly for educational, research, and defensive purposes only. 

You are explicitly prohibited from using any materials contained herein to access, test, modify, or exploit any device, network, or system that you do not own 100% or for which you do not have explicit, documented, and legally binding authorization to interact with.

By using this repository and course, you acknowledge and agree that:

1. Any illegal, unauthorized, or malicious use of this information is solely your responsibility.
2. The author(s) and contributor(s) of this repository and course shall not be held liable for any damages, legal repercussions, criminal charges, or unauthorized actions resulting from the use, misuse, or abuse of the contents herein.
3. You will comply with all applicable local, state, national, and international laws regarding cybersecurity and computer fraud.

**IF YOU DO NOT AGREE WITH THESE TERMS, DO NOT USE THIS REPOSITORY AND COURSE.**
***

<br>
<br>

> Hello, friend.
>
> The wall unit swore the room had been quiet all night. No motion. No sound. Just a
> tidy little beacon every sixty seconds, humming off to a relay nobody in the building
> had ever heard of.
>
> Then we pulled the flash and found nothing - the sweep crew's kit had cooked every
> image on the chip. Boot, environment, kernel, rootfs: a few dozen bytes of header,
> then zeros.
>
> But we caught the node mid-transmission, and one thing survived: **the application
> binary**. No names. No source. Just the daemon that watches, routes, and whispers.
>
> You have the binary, a host, and Ghidra. What you do not have is time: the sweep
> reaches this block at dawn.

This is the companion capture-the-flag to the
[telescreen](https://github.com/mytechnotalent/telescreen) project. Where the project
builds the defended device, this CTF hands you the **compromised** daemon and asks you
to reverse it, find every defect, prove it, and rebuild it hardened.

<br>

## WHERE THIS FITS

This CTF sits in the same world as OPERATION COLD IRON. The Ministry runs the
state - the surveillance, the cold chain, the gates, the pipelines - and against
it stands WHITEOUT. OPERATION COLD IRON is a planned **ten-act saga** (still in
development); the acts build the Ministry's industrial edge, starting with the
[cold-chain monitor](https://github.com/mytechnotalent/cold-chain-monitor).
**TELESCREEN is the surveillance backbone that watches it**, and this repository
is that backbone **captured and compromised** - the finale after OPERATION COLD
IRON. The whole saga is **ARM** - bare-metal Cortex-M33 in the acts,
application-class Cortex-A here.

| work | platform | role in the story |
| ---- | -------- | ----------------- |
| [OPERATION COLD IRON](https://github.com/mytechnotalent/cold-chain-monitor) | ARM Cortex-M33 (RP2350) | the Ministry's cold-chain edge - Act I (saga in development) |
| [telescreen](https://github.com/mytechnotalent/telescreen) | ARM Cortex-A76 (Raspberry Pi 5) | the defended surveillance backbone |
| **CTF_telescreen (this repo)** | **ARM Cortex-A (aarch64 ELF)** | **the same daemon, compromised** |

<br>

## THE MISSION

`firmware/ctfnode.stripped` is the TELESCREEN node daemon with deliberate defects.
Reverse the stripped aarch64 binary, give every function its name back, find the
backdoors, break the weak key derivation, and produce a hardened replacement.

> **No Raspberry Pi 5 - or any hardware - is required.** This CTF is a Ghidra
> exercise. You reverse the stripped aarch64 ELF on any host; the live defect
> harnesses run in a pinned `linux/arm64` Docker container (emulated on Windows
> x64, Linux x64, and macOS). There is nothing to buy, flash, or boot. Ghidra plus
> Docker is the whole lab.

| # | Defect | What the Ministry did |
|---|--------|-----------------------|
| B1 | Config-sourced root exec | runs every `run=` line of a writable config as root |
| B2 | Command injection | builds `ping -c 1 <query>` and `system()`s it |
| B3 | Archive-to-root restore | runs `tar -xvzf <upload> -C /` as root |
| B4 | Empty / default credentials | accepts `admin` with an empty password |
| B5 | Debug root shell | leaves `system("/bin/sh")` in the production path |
| B6 | Weak key schedule | derives the beacon key from the public UID via a reflected CRC-32 |

> **Threat model:** all of these are **local** flaws in the node's own command
> surface - reachable by invoking the daemon or influencing a file/query it consumes.
> There is no network listener in this binary. "Remote root" is not a correct
> description.

<br>

## THE ARTIFACTS

```
firmware/ctfnode.stripped    ELF 64-bit LSB, ARM aarch64, stripped - the target
firmware/ctfnode.unstripped  the same code with names - the instructor answer key
ctf/ctfnode.c                the vulnerable source (instructors)
```

Artifact identity:

```text
ctfnode.stripped   af7ab5c2b4837083682db8b54f6892b1a2a33dcc8ce7b202b5a4a5163232da6d
ctfnode.unstripped 6bcee7daa91280eaf02558b1b5f1b5cc8e22a84179605a0725af2b5564257e0a
```

<br>

## THE CURRICULUM - every document in this repository

### Documents

| document | role |
| -------- | ---- |
| [CTF-XX-I.md](CTF-XX-I.md) / [.pdf](CTF-XX-I.pdf) | student instructions |
| [CTF-XX-R.md](CTF-XX-R.md) / [.pdf](CTF-XX-R.pdf) | requirements and grading |
| [CTF-XX-S.md](CTF-XX-S.md) / [.pdf](CTF-XX-S.pdf) | instructor solution key |
| [DESIGN.md](DESIGN.md) | the build spine (instructor-facing) |
| [PARTS.md](PARTS.md) | optional hardware notes (not required for the RE task) |

### Reverse-engineering the node (stripped aarch64 binary)

| artefact | role |
| -------- | ---- |
| [firmware/README.md](firmware/README.md) | the stripped target and the answer key |
| [firmware/build_target.sh](firmware/build_target.sh) | builds the target (cross-platform, pinned container) |
| [ghidra/README.md](ghidra/README.md) | the Ghidra workspace |
| [ghidra/RESOLUTION_MAP.md](ghidra/RESOLUTION_MAP.md) | every function -> its real name + the proving rule |
| [ghidra/resolution.json](ghidra/resolution.json) | the resolution data, machine-readable |
| [CTF-XX-J-ghidra-function-resolution.md](CTF-XX-J-ghidra-function-resolution.md) | the per-function RE report (with call graphs and decompiled C) |
| [ctf/ctfnode.c](ctf/ctfnode.c) | the vulnerable source (instructors only) |
| [scripts/test_consistency.py](scripts/test_consistency.py) | regression: the compiled binary's key must equal the Python tool and the published vector (run by CI) |
| [scripts/test_defects.py](scripts/test_defects.py) | live defect harness: proves B1-B6 actually manifest (containerized, no hardware) |
| [scripts/weak_decrypt.py](scripts/weak_decrypt.py) | reference implementation of the weak key schedule |
| [ghidra/tests/test_resolution.py](ghidra/tests/test_resolution.py) | asserts the function-resolution invariants |

### Setup (Windows x64, Linux x64, macOS arm64)

Install Docker, the JDK 21, and Ghidra 12.1.3 using the companion course:
**`telescreen` -> [docs/31-prerequisites-and-install.md](https://github.com/mytechnotalent/telescreen/blob/main/docs/31-prerequisites-and-install.md)**,
then the lab sheets
[docs/walkthrough/75](https://github.com/mytechnotalent/telescreen/blob/main/docs/walkthrough/75-prereqs-and-install.md),
[76](https://github.com/mytechnotalent/telescreen/blob/main/docs/walkthrough/76-ghidra-from-zero.md), and
[77](https://github.com/mytechnotalent/telescreen/blob/main/docs/walkthrough/77-function-resolution.md).

<br>

## QUICK START

```bash
./firmware/build_target.sh            # build ctfnode.stripped + ctfnode.unstripped
./ghidra/make_project.sh              # headless analysis -> ghidra/proj/CTFNodeRE.gpr
python3 scripts/test_defects.py       # prove B1-B5 live
python3 scripts/test_consistency.py   # prove B6 against the Python tool
```

<br>

## RELATED

- Project: [telescreen](https://github.com/mytechnotalent/telescreen) - the defended lab
- Course: [Embedded Hacking](https://github.com/mytechnotalent/Embedded-Hacking)

<br>

# License
[MIT License](https://github.com/mytechnotalent/CTF_telescreen/blob/main/LICENSE)
