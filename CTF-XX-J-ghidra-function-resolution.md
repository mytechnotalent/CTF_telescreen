# Appendix J - Function-by-Function Reverse Engineering

This appendix is the complete reverse-engineering record of the stripped
target `firmware/ctfnode.stripped`.  For every one of the 10 application
functions it gives the address, the meaningless label Ghidra shows, what
the function really is, the call graph around it extracted from the real
machine code, the evidence that resolves it, and its decompiled body.

Everything here is reproducible from `firmware/ctfnode.stripped` alone plus
the instructor's `firmware/ctfnode.unstripped` answer key.

> **The four resolution rules** (see `ghidra/RESOLUTION_MAP.md`):
>
> - **R1** exact address match against the unstripped twin (certain),
> - **R2** `.plt` stub -> `JUMP_SLOT` relocation -> import name (certain),
> - **R3** the `.plt` PLT0 lazy resolver (certain),
> - **R4** phantom/overlapping function on alignment padding (certain).

---

## `0x00400960` - `ctf_crc32_le`  (ctfnode)

- **Ghidra shows:** `FUN_00400960` (a stripped binary has no names).
- **Resolved name:** `ctf_crc32_le`
- **Module:** `ctf/ctfnode.c`
- **Role:** Compute the reflected crc32_le used by the node's key schedule.
- **Evidence:** R1: exact nm match against the unstripped twin.
- **Called by:** _(entry points only)_
- **Calls:** _(leaf function)_

```c
uint FUN_00400960(uint param_1,byte *param_2,ulong param_3)

{
  uint uVar1;
  byte *pbVar2;
  byte *pbVar3;
  int iVar4;
  
  if (param_3 != 0) {
    pbVar3 = param_2 + param_3;
    do {
      uVar1 = param_1 ^ *param_2;
      iVar4 = 8;
      do {
        iVar4 = iVar4 + -1;
        uVar1 = -(uVar1 & 1) & 0xedb88320 ^ uVar1 >> 1;
      } while (iVar4 != 0);
      param_2 = param_2 + 1;
      param_1 = uVar1;
    } while (pbVar3 != param_2);
  }
  return param_1;
}
```

## `0x004009b0` - `ctf_weak_key`  (ctfnode)

- **Ghidra shows:** `FUN_004009b0` (a stripped binary has no names).
- **Resolved name:** `ctf_weak_key`
- **Module:** `ctf/ctfnode.c`
- **Role:** DEFECT B6 - derive the beacon key from the PUBLIC device UID.
- **Evidence:** R1: exact nm match against the unstripped twin.
- **Called by (1):** `ctf_dispatch`
- **Calls (1):** `strlen@plt`

```c

void FUN_004009b0(byte *param_1,long param_2)

{
  size_t sVar1;
  uint uVar2;
  int iVar3;
  byte *pbVar4;
  long lVar5;
  
  sVar1 = strlen((char *)param_1);
  uVar2 = 0;
  if (sVar1 != 0) {
    pbVar4 = param_1;
    do {
      iVar3 = 8;
      uVar2 = uVar2 ^ *pbVar4;
      do {
        iVar3 = iVar3 + -1;
        uVar2 = -(uVar2 & 1) & 0xedb88320 ^ uVar2 >> 1;
      } while (iVar3 != 0);
      pbVar4 = pbVar4 + 1;
    } while (pbVar4 != param_1 + sVar1);
  }
  lVar5 = 0;
  if (sVar1 != 0) {
    pbVar4 = param_1;
    do {
      do {
        iVar3 = 8;
        uVar2 = uVar2 ^ *pbVar4;
        do {
          iVar3 = iVar3 + -1;
          uVar2 = -(uVar2 & 1) & 0xedb88320 ^ uVar2 >> 1;
        } while (iVar3 != 0);
        pbVar4 = pbVar4 + 1;
      } while (pbVar4 != param_1 + sVar1);
      *(char *)(param_2 + lVar5) = (char)uVar2;
      lVar5 = lVar5 + 1;
      pbVar4 = param_1;
    } while (lVar5 != 0x20);
    return;
  }
  do {
    *(char *)(param_2 + lVar5) = (char)uVar2;
    lVar5 = lVar5 + 1;
  } while (lVar5 != 0x20);
  return;
}
```

## `0x00400a8c` - `ctf_login`  (ctfnode)

- **Ghidra shows:** `FUN_00400a8c` (a stripped binary has no names).
- **Resolved name:** `ctf_login`
- **Module:** `ctf/ctfnode.c`
- **Role:** DEFECT B4 - authenticate with hard-coded default credentials.
- **Evidence:** R1: exact nm match against the unstripped twin.
- **Called by:** _(entry points only)_
- **Calls (1):** `strcmp@plt`

```c

bool FUN_00400a8c(char *param_1,char *param_2)

{
  bool bVar1;
  int iVar2;
  
  bVar1 = false;
  if (param_1 != (char *)0x0 && param_2 != (char *)0x0) {
    bVar1 = false;
    iVar2 = strcmp(param_1,"admin");
    if (iVar2 == 0) {
      bVar1 = *param_2 == '\0';
    }
  }
  return bVar1;
}
```

## `0x00400ae0` - `ctf_config_run`  (ctfnode)

- **Ghidra shows:** `FUN_00400ae0` (a stripped binary has no names).
- **Resolved name:** `ctf_config_run`
- **Module:** `ctf/ctfnode.c`
- **Role:** DEFECT B1 - source a writable config file as root.
- **Evidence:** R1: exact nm match against the unstripped twin.
- **Called by (1):** `ctf_dispatch`
- **Calls (4):** `fclose@plt`, `fopen@plt`, `system@plt`, `fgets@plt`

```c

undefined8 FUN_00400ae0(char *param_1)

{
  FILE *__stream;
  char *pcVar1;
  undefined8 uVar2;
  int local_100;
  char acStack_fc [252];
  
  __stream = fopen(param_1,"r");
  if (__stream == (FILE *)0x0) {
    uVar2 = 0xffffffff;
  }
  else {
    while (pcVar1 = fgets((char *)&local_100,0x100,__stream), pcVar1 != (char *)0x0) {
      while (local_100 == 0x3d6e7572) {
        system(acStack_fc);
        pcVar1 = fgets((char *)&local_100,0x100,__stream);
        if (pcVar1 == (char *)0x0) goto LAB_00400b44;
      }
    }
LAB_00400b44:
    fclose(__stream);
    uVar2 = 0;
  }
  return uVar2;
}
```

## `0x00400b64` - `ctf_build_cmd`  (ctfnode)

- **Ghidra shows:** `FUN_00400b64` (a stripped binary has no names).
- **Resolved name:** `ctf_build_cmd`
- **Module:** `ctf/ctfnode.c`
- **Role:** Build a shell command from a request string (defect B2, part 1).
- **Evidence:** R1: exact nm match against the unstripped twin.
- **Called by:** _(entry points only)_
- **Calls (1):** `snprintf@plt`

```c

int FUN_00400b64(undefined8 param_1,char *param_2,size_t param_3)

{
  int iVar1;
  
  iVar1 = snprintf(param_2,param_3,"ping -c 1 %s",param_1);
  return iVar1;
}
```

## `0x00400b80` - `ctf_http_handle`  (ctfnode)

- **Ghidra shows:** `FUN_00400b80` (a stripped binary has no names).
- **Resolved name:** `ctf_http_handle`
- **Module:** `ctf/ctfnode.c`
- **Role:** DEFECT B2 - run the command built from a request string.
- **Evidence:** R1: exact nm match against the unstripped twin.
- **Called by (1):** `ctf_dispatch`
- **Calls (2):** `snprintf@plt`, `system@plt`

```c

int FUN_00400b80(undefined8 param_1)

{
  int iVar1;
  char acStack_200 [512];
  
  snprintf(acStack_200,0x200,"ping -c 1 %s",param_1);
  iVar1 = system(acStack_200);
  return iVar1;
}
```

## `0x00400bc0` - `ctf_restore`  (ctfnode)

- **Ghidra shows:** `FUN_00400bc0` (a stripped binary has no names).
- **Resolved name:** `ctf_restore`
- **Module:** `ctf/ctfnode.c`
- **Role:** DEFECT B3 - restore an uploaded archive directly into root.
- **Evidence:** R1: exact nm match against the unstripped twin.
- **Called by (1):** `ctf_dispatch`
- **Calls (2):** `snprintf@plt`, `system@plt`

```c

int FUN_00400bc0(undefined8 param_1)

{
  int iVar1;
  char acStack_200 [512];
  
  snprintf(acStack_200,0x200,"tar -xvzf %s -C /",param_1);
  iVar1 = system(acStack_200);
  return iVar1;
}
```

## `0x00400c00` - `ctf_debug_shell`  (ctfnode)

- **Ghidra shows:** `FUN_00400c00` (a stripped binary has no names).
- **Resolved name:** `ctf_debug_shell`
- **Module:** `ctf/ctfnode.c`
- **Role:** DEFECT B5 - drop to a local root debug shell.
- **Evidence:** R1: exact nm match against the unstripped twin.
- **Called by:** _(entry points only)_
- **Calls (1):** `system@plt`

```c

int FUN_00400c00(void)

{
  int iVar1;
  
  iVar1 = system("/bin/sh");
  return iVar1;
}
```

## `0x00400c0c` - `ctf_banner`  (ctfnode)

- **Ghidra shows:** `FUN_00400c0c` (a stripped binary has no names).
- **Resolved name:** `ctf_banner`
- **Module:** `ctf/ctfnode.c`
- **Role:** Print the node banner.
- **Evidence:** R1: exact nm match against the unstripped twin.
- **Called by:** _(entry points only)_
- **Calls (1):** `puts@plt`

```c

int FUN_00400c0c(void)

{
  int iVar1;
  
  iVar1 = puts("TELESCREEN node - the wall unit sees you");
  return iVar1;
}
```

## `0x00400c20` - `ctf_dispatch`  (ctfnode)

- **Ghidra shows:** `FUN_00400c20` (a stripped binary has no names).
- **Resolved name:** `ctf_dispatch`
- **Module:** `ctf/ctfnode.c`
- **Role:** Dispatch a command line to the node features.
- **Evidence:** R1: exact nm match against the unstripped twin.
- **Called by (1):** `main`
- **Calls (9):** `putc@plt`, `system@plt`, `puts@plt`, `strcmp@plt`, `printf@plt`, `ctf_weak_key`, `ctf_config_run`, `ctf_http_handle`, `ctf_restore`

```c

ulong FUN_00400c20(int param_1,long param_2)

{
  int iVar1;
  uint uVar2;
  ulong uVar3;
  byte *pbVar4;
  char *pcVar6;
  byte abStack_20 [32];
  byte *pbVar5;
  
  if (param_1 < 2) {
    puts("TELESCREEN node - the wall unit sees you");
    return 0;
  }
  pcVar6 = *(char **)(param_2 + 8);
  iVar1 = strcmp(pcVar6,"config");
  if (iVar1 == 0) {
    if (param_1 != 2) {
      uVar3 = FUN_00400ae0(*(undefined8 *)(param_2 + 0x10));
      return uVar3;
    }
LAB_00400c60:
    iVar1 = strcmp(pcVar6,"restore");
    if (iVar1 == 0) goto LAB_00400c74;
    iVar1 = strcmp(pcVar6,"shell");
  }
  else {
    iVar1 = strcmp(pcVar6,"http");
    if (iVar1 == 0) {
      if (param_1 != 2) {
        uVar3 = FUN_00400b80(*(undefined8 *)(param_2 + 0x10));
        return uVar3;
      }
      goto LAB_00400c60;
    }
    iVar1 = strcmp(pcVar6,"restore");
    if (iVar1 != 0) {
      iVar1 = strcmp(pcVar6,"login");
      if (iVar1 == 0 && 3 < param_1) {
        pcVar6 = *(char **)(param_2 + 0x18);
        if (*(char **)(param_2 + 0x10) == (char *)0x0 || pcVar6 == (char *)0x0) {
          return 1;
        }
        iVar1 = strcmp(*(char **)(param_2 + 0x10),"admin");
        if (iVar1 != 0) {
          return 1;
        }
        return (ulong)(*pcVar6 != '\0');
      }
      iVar1 = strcmp(pcVar6,"shell");
      if (iVar1 == 0) goto LAB_00400d58;
      iVar1 = strcmp(pcVar6,"key");
      if (iVar1 == 0 && param_1 != 2) {
        FUN_004009b0(*(undefined8 *)(param_2 + 0x10),abStack_20);
        pbVar5 = abStack_20;
        do {
          pbVar4 = pbVar5 + 1;
          printf("%02x",(ulong)*pbVar5);
          pbVar5 = pbVar4;
        } while (&stack0x00000000 != pbVar4);
        putc(10,stdout);
        return 0;
      }
      goto LAB_00400c88;
    }
    if (param_1 != 2) {
      uVar3 = FUN_00400bc0(*(undefined8 *)(param_2 + 0x10));
      return uVar3;
    }
LAB_00400c74:
    iVar1 = strcmp(pcVar6,"shell");
  }
  if (iVar1 == 0) {
LAB_00400d58:
    uVar2 = system("/bin/sh");
    return (ulong)uVar2;
  }
LAB_00400c88:
  puts("TELESCREEN node - the wall unit sees you");
  return 2;
}
```

---

## Reverse-engineering lessons this binary teaches

### Lesson 1 - Static helpers are inlined away

The source has more functions than the compiled binary.  A student who
greps the stripped listing for a helper name will not find it, because the
compiler inlined every `static` one:

- `ctf_crc32_byte` is inlined into both `ctf_crc32_le` and `ctf_weak_key`,
  so the reflected fold appears **twice** as straight-line machine code.
- `ctf_cmd`, `ctf_print_key`, `ctf_try_path`, and `ctf_try_misc` are inlined
  into `ctf_dispatch`, which is why the dispatcher is the largest function.

Always read the call graph, not just the symbol count, before concluding a
function is missing.

### Lesson 2 - Phantom functions on alignment padding

Modern toolchains align functions to 16 bytes and pad with `nop`.  Ghidra
can mistake the padding for the start of a small function, producing a
phantom that overlaps the real one:

- `0x00400adc` is a phantom whose body is identical to `ctf_config_run`
  (`0x00400ae0`) sitting on the 4-byte alignment pad.

Always confirm a function's true entry with the call graph and the
prologue (`stp x29, x30, [sp, #-N]!`), never by Ghidra's guess alone.

### Lesson 3 - The PLT and the GOT

Every imported libc function is indirected through the `.plt`: the stub
loads a slot from `.got.plt` and branches to it (`br x17`).  The relocation
at `0x420000`-`0x420060` names the target, so `bl 0x400770` is `system`, not
some anonymous `FUN_`.  Reading the `.rela.plt` relocations is how a
reverse engineer recovers library calls from a stripped binary.

