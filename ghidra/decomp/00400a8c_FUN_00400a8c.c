
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

