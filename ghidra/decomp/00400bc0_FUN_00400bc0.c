
int FUN_00400bc0(undefined8 param_1)

{
  int iVar1;
  char acStack_200 [512];
  
  snprintf(acStack_200,0x200,"tar -xvzf %s -C /",param_1);
  iVar1 = system(acStack_200);
  return iVar1;
}

