strr = [0x73,0x79,0x6e,0x74,0x39,0x09,0x76,0x70,0x72,0x23,0x17,0x79,0x6e,0x74,0x23,0x76,0x66,0x23,0x75,0x72,0x65,0x72,0x23,0x1c,0x65,0x72,0x23,0x6c,0x62,0x68,0x17,0x76,0x61,0x71,0x2a,0x2a,0x2a,0x36]
flag= ''
mark = 0
for i in range(38):
    if strr[i]>=97 and strr[i]<=122:
        #print(i)
        flag += chr(((strr[i] - 97 + 13) % 26) + 97)
    elif strr[i]^0x4f>=65 and strr[i]^0x4f<=90:
        tmp = strr[i]^0x4f
        #print(tmp,i)
        tmp = ((tmp - 65  - 5) % 26) + 65
        tmp = ((tmp - 65  + 13) % 26) + 65
        flag += chr(tmp)
    elif strr[i]==35 :
        flag += '_'
    elif strr[i]== 42 :
        flag += '!'
    elif strr[i]==54:
        flag += '}'
    elif strr[i]==57:
        flag += '{'       
    else:
        flag += chr(strr[i])
print(flag)
#flag{Nice_Flag_is_here_Are_youFind!!!}
