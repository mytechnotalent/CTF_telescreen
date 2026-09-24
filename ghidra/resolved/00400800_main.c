
ulong thunk_FUN_00400c20(int param_1,long param_2)

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

