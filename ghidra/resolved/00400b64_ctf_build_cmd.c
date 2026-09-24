
int FUN_00400b64(undefined8 param_1,char *param_2,size_t param_3)

{
  int iVar1;
  
  iVar1 = snprintf(param_2,param_3,"ping -c 1 %s",param_1);
  return iVar1;
}

