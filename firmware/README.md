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

`build_target.sh` prints the SHA-256 of each file. Addresses for every function
are in `../ghidra/RESOLUTION_MAP.md`.
