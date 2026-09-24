
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

