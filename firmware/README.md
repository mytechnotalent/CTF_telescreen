# firmware/ - the CTF node (stripped vulnerable target)

This folder holds the **vulnerable** application the student reverses.

| file | what it is | who uses it |
| ---- | ---------- | ----------- |
| `build_target.sh` | builds both files below from `../ctf/ctfnode.c` | everyone |
| `ctfnode.stripped` | the **stripped** ARM64 target - no names | students |
| `ctfnode.unstripped` | the same code **with** names - the answer key | instructors |

## Build it

```bash
./firmware/build_target.sh
```

It runs in a pinned `linux/arm64` Docker container, so the output is identical on
Windows x64, Linux x64, and macOS arm64. Install Docker, the JDK, and Ghidra
using the companion course, **`telescreen` → `docs/31-prerequisites-and-install.md`**.

## What the student must find

The node contains six defects. Each is a function in `../ctf/ctfnode.c` and a
`FUN_00xxxxxx` in the stripped binary:

| defect | function | what it is |
| ------ | -------- | ---------- |
| B1 | `ctf_config_run` | sources a writable config as root |
| B2 | `ctf_http_handle` / `ctf_build_cmd` | builds and runs a shell command from a request |
| B3 | `ctf_restore` | `tar -xvzf <upload> -C /` as root |
| B4 | `ctf_login` | hard-coded default credentials (`admin` / empty) |
| B5 | `ctf_debug_shell` | `system("/bin/sh")` |
| B6 | `ctf_weak_key` | beacon key derived from the public UID |

## Prove you have the right bytes

`build_target.sh` prints the SHA-256 of each file. The instructor-issued values are:

```text
ctfnode.stripped   af7ab5c2b4837083682db8b54f6892b1a2a33dcc8ce7b202b5a4a5163232da6d
ctfnode.unstripped 6bcee7daa91280eaf02558b1b5f1b5cc8e22a84179605a0725af2b5564257e0a
```

Addresses for every function are in `../ghidra/RESOLUTION_MAP.md`.

> **Note on the threat model.** B1, B2, B3, and B5 are **local** `system()` flaws
> reachable through the node's own subcommands; there is no network listener in this
> binary. B4 is a credential flaw and B6 is a public-identifier key schedule.
