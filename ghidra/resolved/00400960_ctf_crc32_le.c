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
