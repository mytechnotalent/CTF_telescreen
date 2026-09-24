
void FUN_00400960(undefined8 param_1,long param_2,long param_3)

{
  int iVar1;
  
  if (param_3 != 0) {
    param_3 = param_2 + param_3;
    do {
      iVar1 = 8;
      do {
        iVar1 = iVar1 + -1;
      } while (iVar1 != 0);
      param_2 = param_2 + 1;
    } while (param_3 != param_2);
  }
  return;
}

