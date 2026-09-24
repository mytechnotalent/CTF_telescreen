
int FUN_00400b80(undefined8 param_1)

{
  int iVar1;
  char acStack_200 [512];
  
  snprintf(acStack_200,0x200,"ping -c 1 %s",param_1);
  iVar1 = system(acStack_200);
  return iVar1;
}

