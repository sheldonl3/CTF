from pwn import *
import math

'''
北京公司24年ctf
┌──(kali㉿kali)-[~/Desktop]
└─$ ./pwn             
Let's play a game, win a hundred rounds and I will give you the flag
round 0: 6694 - 9900 = ?
give me result: -3206
right!
round 1: 4949 / 3676 = ?
give me result: 

'''

io = remote("10.11.0.9", 9999)

for i in range(100):
    print(i)
    io.recvuntil(b":")
    express = io.recvuntil(b" =?", drop=True).decode()
    if '/' in express:
        io.sendlineafter(b"result:",str(math.floor(eval(express))).encode())
    else:
        io.sendlineafter(b"result:",str((eval(express))).encode())
io.interactive()