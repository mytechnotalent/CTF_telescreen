# TELESCREEN - Function Resolution Map

Every function Ghidra found in the stripped target, resolved to a
real identity, with the evidence that proves it.  Totals:

- **10** application functions (our firmware code)
- **28** imported-library thunks (OpenSSL / glibc)
- **1** phantom functions (alignment padding)
- **11** C runtime / start-up functions
- **50** total functions in the binary

## Application functions (resolved 1:1 against the unstripped twin)

| address | Ghidra label | resolved name | module | role |
| ------- | ------------ | ------------- | ------ | ---- |
| `0x00400960` | `FUN_00400960` | `ctf_crc32_le` | ctfnode | Compute the reflected crc32_le used by the node's key schedule. |
| `0x004009b0` | `FUN_004009b0` | `ctf_weak_key` | ctfnode | DEFECT B6 - derive the beacon key from the PUBLIC device UID. |
| `0x00400a8c` | `FUN_00400a8c` | `ctf_login` | ctfnode | DEFECT B4 - authenticate with hard-coded default credentials. |
| `0x00400ae0` | `FUN_00400ae0` | `ctf_config_run` | ctfnode | DEFECT B1 - source a writable config file as root. |
| `0x00400b64` | `FUN_00400b64` | `ctf_build_cmd` | ctfnode | Build a shell command from a request string (defect B2, part 1). |
| `0x00400b80` | `FUN_00400b80` | `ctf_http_handle` | ctfnode | DEFECT B2 - run the command built from a request string. |
| `0x00400bc0` | `FUN_00400bc0` | `ctf_restore` | ctfnode | DEFECT B3 - restore an uploaded archive directly into root. |
| `0x00400c00` | `FUN_00400c00` | `ctf_debug_shell` | ctfnode | DEFECT B5 - drop to a local root debug shell. |
| `0x00400c0c` | `FUN_00400c0c` | `ctf_banner` | ctfnode | Print the node banner. |
| `0x00400c20` | `FUN_00400c20` | `ctf_dispatch` | ctfnode | Dispatch a command line to the node features. |

## Imported-library thunks

| address | resolved name |
| ------- | ------------- |
| `0x00400710` | `strlen` |
| `0x00400720` | `__libc_start_main` |
| `0x00400730` | `putc` |
| `0x00400740` | `snprintf` |
| `0x00400750` | `fclose` |
| `0x00400760` | `fopen` |
| `0x00400770` | `system` |
| `0x00400780` | `__gmon_start__` |
| `0x00400790` | `abort` |
| `0x004007a0` | `puts` |
| `0x004007b0` | `strcmp` |
| `0x004007c0` | `printf` |
| `0x004007d0` | `fgets` |
| `0x00421000` | `strlen` |
| `0x00421008` | `__libc_start_main` |
| `0x00421010` | `_ITM_deregisterTMCloneTable` |
| `0x00421018` | `putc` |
| `0x00421020` | `snprintf` |
| `0x00421028` | `fclose` |
| `0x00421030` | `fopen` |
| `0x00421038` | `system` |
| `0x00421040` | `__gmon_start__` |
| `0x00421048` | `abort` |
| `0x00421050` | `puts` |
| `0x00421058` | `strcmp` |
| `0x00421060` | `_ITM_registerTMCloneTable` |
| `0x00421068` | `printf` |
| `0x00421070` | `fgets` |

## Phantom functions (Ghidra artefacts - NOT real functions)

- `0x00400adc` (`FUN_00400adc`): R4: identical body to FUN_00400ae0; alignment padding

## C runtime / start-up

- `0x004006c8` (`_DT_INIT`) -> `_init`
- `0x004006f0` (`FUN_004006f0`) -> `<.plt> PLT0 resolver`
- `0x00400800` (`thunk_FUN_00400c20`) -> `main`
- `0x00400840` (`entry`) -> `_start`
- `0x00400880` (`FUN_00400880`) -> `_dl_relocate_static_pie`
- `0x00400888` (`FUN_00400888`) -> `call_weak_fn`
- `0x004008a0` (`FUN_004008a0`) -> `deregister_tm_clones`
- `0x004008d0` (`FUN_004008d0`) -> `register_tm_clones`
- `0x0040090c` (`_FINI_0`) -> `__do_global_dtors_aux`
- `0x00400940` (`_INIT_0`) -> `frame_dummy`
- `0x00400e44` (`_DT_FINI`) -> `_fini`

