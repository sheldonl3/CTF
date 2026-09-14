data='e3nifIH9b_C@n@dH'
data=list(data)
for i in range(len(data)):
    data[i]=chr(ord(data[i])-i)
print(data)
res=''
for i in range(len(data)):
    res+=data[i]
print(res)


'''
print("please enter the flag:", v7);
  scanf("%20s", (char)Str);
  v3 = j_strlen(Str);
  v4 = (const char *)sub_4110BE(Str, v3, v14);   #base64
  strncpy(Destination, v4, '(');
  v11 = j_strlen(Destination);
  for ( j = 0; j < v11; ++j )                   #base64之后加i
    Destination[j] += j;
  v5 = j_strlen(Destination);
  if ( !strncmp(Destination, Str2, v5) )
    print("rigth flag!\n", v8);
  else
    print("wrong flag!\n", v8);
  return 0;

'''