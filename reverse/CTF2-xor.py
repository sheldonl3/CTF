data='f\nk\fw&O.@\x11x\rZ;U\x11p\x19F\x1Fv\"M#D\x0Eg\x06h\x0FG2O'
data=list(data)
for i in range(len(data)-1,1,-1):
    data[i]=chr(ord(data[i])^ord(data[i-1]))
res=''
for i in range(len(data)):
    res+=data[i]
print(res)


'''
printf("Input your flag:\n");
  get_line(__b, 256LL);
  if ( strlen(__b) != 33 )
    goto LABEL_7;
  for ( i = 1; i < 33; ++i )
    __b[i] ^= __b[i - 1];             连续异或，这样反向异或
  if ( !strncmp(__b, global, 0x21uLL) )
    printf("Success");
  else
LABEL_7:
    printf("Failed");
'''