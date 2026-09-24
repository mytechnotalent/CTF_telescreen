
undefined8 FUN_00400adc(char *param_1)

{
  FILE *__stream;
  char *pcVar1;
  undefined8 uVar2;
  int iStack_100;
  char acStack_fc [252];
  
  __stream = fopen(param_1,"r");
  if (__stream == (FILE *)0x0) {
    uVar2 = 0xffffffff;
  }
  else {
    while (pcVar1 = fgets((char *)&iStack_100,0x100,__stream), pcVar1 != (char *)0x0) {
      while (iStack_100 == 0x3d6e7572) {
        system(acStack_fc);
        pcVar1 = fgets((char *)&iStack_100,0x100,__stream);
        if (pcVar1 == (char *)0x0) goto LAB_00400b44;
      }
    }
LAB_00400b44:
    fclose(__stream);
    uVar2 = 0;
  }
  return uVar2;
}

