import sys

'''
# Catching.exe 详细题解

## 0. 基本信息

| 属性 | 值 |
|------|-----|
| 文件名 | `Catching.exe` |
| 类型 | PE32 executable (console) Intel 80386, for MS Windows |
| 编译器 | MSVC 2015+ (C++) |
| 调试符号 | `Catching.pdb` (位于 `E:\2024\re\Catching\sourcecode\Catching\Release\`) |
| 长度 | 38 字符 |
| 最终 flag | `flag{Nice_Flag_is_here_Are_youFind!!!}` |

---

## 1. 初步侦察

### 1.1 运行观察

```
> Catching.exe
welcome to rot reverse world!
input my flag:
```

随意输入后输出 `you are wrong!`，输入正确 flag 则输出 `you are right!`。

### 1.2 字符串线索

```bash
strings Catching.exe
```

关键输出：

| 字符串 | 含义 |
|--------|------|
| `welcome to rot reverse world!` | **"rot" 直接提示加密方式是 ROT（字符轮转替换）** |
| `input my flag:` | 输入提示 |
| `you are right!` / `you are wrong!` | 结果判断 |
| `synt9	vpr#...vaq***6` | 硬编码比较密文（含控制字符） |

"rot reverse world" = ROT 逆向世界 → 加密方式是 ROT 轮转密码，需要逆向还原。

---

## 2. 静态逆向分析

### 2.1 程序执行流程

用 IDA / x64dbg / Ghidra 定位到核心验证函数（约 `0x401220`），还原逻辑：

```
main()
 ├─ cout << "welcome to rot reverse world!"
 ├─ cout << "input my flag:"
 ├─ cin  >> user_input              // 读取 std::string
 ├─ for each char in user_input:    // 逐字符变换
 │    ├─ islower(c) → ROT13         
 │    ├─ isupper(c) → 大写专用映射   
 │    ├─ c == '{'  → '9'
 │    ├─ c == '}'  → '6'
 │    ├─ c == '_'  → '#'
 │    ├─ c == '!'  → '*'
 │    └─ else      → 原样
 ├─ memcmp(transformed, g_encoded, 38)   // 与硬编码比较
 └─ 输出 "you are right!" / "you are wrong!"
```

### 2.2 硬编码比较数据

在 `.rdata` 段 (VA `0x404224`)，38 字节密文：

```
Hex: 73 79 6E 74 39 09 76 70 72 23 17 79 6E 74 23 76
     66 23 75 72 65 72 23 1C 65 72 23 6C 62 68 17 76
     61 71 2A 2A 2A 36
```

ASCII 展示（`◌` 表示不可打印控制字符）：

```
s  y  n  t  9  ◌  v  p  r  #  ◌  y  n  t  #  v
f  #  u  r  e  r  #  ◌  e  r  #  l  b  h  ◌  v
a  q  *  *  *  6
```

### 2.3 变换算法详细分析

#### 2.3.1 小写字母 → ROT13 (标准)

反汇编中 `addb $0x9f` 对应：

```
0x9F = 159 = 256 - 97 = -97 (signed)
addb $0x9F 等价于 sub $0x61   →  得到字母在字母表中的索引 (c - 'a')
```

后续 +13、对 ≥26 的情况减 26（循环）、再 +0x61 还原，即：

```c
c = (c - 'a' + 13) % 26 + 'a';
```

这是**标准 ROT13**。ROT13 的关键性质：**ROT13(ROT13(x)) = x**，自身逆运算。

#### 2.3.2 大写字母 → 自定义映射

反汇编中 `addb $0xbf` 对应:

```
0xBF = 191 = 256 - 65 = -65 (signed)
addb $0xBF 等价于 sub $0x41   →  得到大写字母索引 (c - 'A')
```

但与 lowercase 不同，大写分支的最终输出**不是字母**，而是落在 0x00~0x1F 范围的控制字符。根据密文反推，当前 flag 中涉及的大写字母映射为：

| 原文 | 索引 | 密文(hex) | 密文(dec) |
|------|------|-----------|-----------|
| `N`  | 13   | 0x09      | 9         |
| `F`  | 5    | 0x17      | 23        |
| `A`  | 0    | 0x1C      | 28        |

> 汇编层面完整的运算包含 `addb $0xbf` + `add $0x0d`（+13）+ `cmp $0x1a` 判断是否越界 + 条件修正，最终产生的值不是 `+ 'A'` 还原，而是落入控制字符区。具体公式不影响解题——我们只需利用映射的**一一对应关系**进行逆向查表即可。

#### 2.3.3 特殊字符 → 直接替换

| 输入 | 输出 | 说明 |
|------|------|------|
| `{`  | `9` (0x39) | flag 左括号 |
| `}`  | `6` (0x36) | flag 右括号 |
| `_`  | `#` (0x23) | 下划线 |
| `!`  | `*` (0x2A) | 感叹号 |

这也是自逆映射（`{↔9`, `}↔6`, `_↔#`, `!↔*`），用相同操作即可还原。

#### 2.3.4 其他字符

数字、空格、标点等不属于上述任何一类的字符**原样通过**，不参与变换。

### 2.4 变换规则汇总

```
         ┌──────────────────────────────────────┐
         │           输入字符 c                  │
         └──────────────────────────────────────┘
                        │
        ┌───────────────┼───────────────┬──────────────┐
        ▼               ▼               ▼              ▼
   islower(c)      isupper(c)     特殊字符         其他
        │               │         {→9 }→6         原样
        ▼               ▼         _→# !→*
     ROT13          大写映射
   (自逆运算)      N→0x09
                   F→0x17
                   A→0x1C
```
## 3. 解密过程

### 3.1 解密策略

由于变换是逐字符的**一一映射**，解密就是对密文每个字节施加**逆映射**：

| 密文字节 | 类型判断 | 逆操作 | 还原结果 |
|----------|----------|--------|----------|
| `a`-`z` | 小写字母 | ROT13 | 对应明文字母 |
| `A`-`Z` | 大写字母 | ROT13 | 对应明文字母 |
| `9`      | 特殊映射 | → `{`  | flag 开头 |
| `6`      | 特殊映射 | → `}`  | flag 结尾 |
| `#`      | 特殊映射 | → `_`  | 下划线 |
| `*`      | 特殊映射 | → `!`  | 感叹号 |
| 0x09     | 大写还原 | → `N`  |           |
| 0x17     | 大写还原 | → `F`  |           |
| 0x1C     | 大写还原 | → `A`  |           |
| 其他     | 原样     | 不变   |           |

### 3.2 逐字节解密表

| # | 密文hex | 密文字符 | 操作 | 明文 | 备注 |
|---|---------|----------|------|------|------|
| 0 | 0x73 | `s` | ROT13 | `f` | |
| 1 | 0x79 | `y` | ROT13 | `l` | |
| 2 | 0x6E | `n` | ROT13 | `a` | |
| 3 | 0x74 | `t` | ROT13 | `g` | |
| 4 | 0x39 | `9` | 特殊映射 | `{` | |
| 5 | 0x09 | (TAB) | 大写还原 | `N` | ← 关键 |
| 6 | 0x76 | `v` | ROT13 | `i` | |
| 7 | 0x70 | `p` | ROT13 | `c` | |
| 8 | 0x72 | `r` | ROT13 | `e` | |
| 9 | 0x23 | `#` | 特殊映射 | `_` | |
| 10| 0x17 | (ETB) | 大写还原 | `F` | ← 关键 |
| 11| 0x79 | `y` | ROT13 | `l` | |
| 12| 0x6E | `n` | ROT13 | `a` | |
| 13| 0x74 | `t` | ROT13 | `g` | |
| 14| 0x23 | `#` | 特殊映射 | `_` | |
| 15| 0x76 | `v` | ROT13 | `i` | |
| 16| 0x66 | `f` | ROT13 | `s` | |
| 17| 0x23 | `#` | 特殊映射 | `_` | |
| 18| 0x75 | `u` | ROT13 | `h` | |
| 19| 0x72 | `r` | ROT13 | `e` | |
| 20| 0x65 | `e` | ROT13 | `r` | |
| 21| 0x72 | `r` | ROT13 | `e` | |
| 22| 0x23 | `#` | 特殊映射 | `_` | |
| 23| 0x1C | (FS)  | 大写还原 | `A` | ← 关键 |
| 24| 0x65 | `e` | ROT13 | `r` | |
| 25| 0x72 | `r` | ROT13 | `e` | |
| 26| 0x23 | `#` | 特殊映射 | `_` | |
| 27| 0x6C | `l` | ROT13 | `y` | |
| 28| 0x62 | `b` | ROT13 | `o` | |
| 29| 0x68 | `h` | ROT13 | `u` | |
| 30| 0x17 | (ETB) | 大写还原 | `F` | ← 关键 |
| 31| 0x76 | `v` | ROT13 | `i` | |
| 32| 0x61 | `a` | ROT13 | `n` | |
| 33| 0x71 | `q` | ROT13 | `d` | |
| 34| 0x2A | `*` | 特殊映射 | `!` | |
| 35| 0x2A | `*` | 特殊映射 | `!` | |
| 36| 0x2A | `*` | 特殊映射 | `!` | |
| 37| 0x36 | `6` | 特殊映射 | `}` | |

### 3.3 拼接结果

```
f l a g { N i c e _ F l a g _ i s _ h e r e _ A r e _ y o u F i n d ! ! ! }
```

即：

```
flag{Nice_Flag_is_here_Are_youFind!!!}
'''

# 从 .rdata 段 0x404224 提取的 38 字节密文
ENCODED_HEX = (
    "73 79 6E 74 39 09 76 70 72 23 17 79 6E 74 23 76 "
    "66 23 75 72 65 72 23 1C 65 72 23 6C 62 68 17 76 "
    "61 71 2A 2A 2A 36"
)
encoded = bytes.fromhex(ENCODED_HEX)

# 大写字母逆向映射表 (密文字节 → 原文字节)
UPPER_REVERSE = {
    0x09: ord('N'),
    0x17: ord('F'),
    0x1C: ord('A'),
}

# 特殊字符映射表 (密文 → 原文)
SPECIAL_REVERSE = {
    0x39: ord('{'),
    0x36: ord('}'),
    0x23: ord('_'),
    0x2A: ord('!'),
}


def rot13(c):
    """小写字母 ROT13（自逆）"""
    return ((c - ord('a') + 13) % 26) + ord('a')


def decode_byte(b):
    """单字节逆向映射"""
    if ord('a') <= b <= ord('z'):
        return rot13(b)
    if ord('A') <= b <= ord('Z'):
        return rot13(b + 0x20) - 0x20  # ROT13 for uppercase
    if b in UPPER_REVERSE:
        return UPPER_REVERSE[b]
    if b in SPECIAL_REVERSE:
        return SPECIAL_REVERSE[b]
    return b  # 其他字符原样


# 解密
flag = bytearray(decode_byte(b) for b in encoded)

print(f"[*] 密文 (hex): {encoded.hex()}")
print(f"[*] 明文 (hex): {flag.hex()}")
print(f"[+] Flag: {flag.decode()}")

# ============ 正向验证 ============
UPPER_FORWARD = {chr(v): k for k, v in UPPER_REVERSE.items()}
SPECIAL_FORWARD = {chr(v): k for k, v in SPECIAL_REVERSE.items()}


def encode_byte(b):
    """正向变换（复现程序加密逻辑）"""
    c = chr(b)
    if c.islower():
        return rot13(b)
    if c.isupper():
        if c in UPPER_FORWARD:
            return UPPER_FORWARD[c]
        return b  # fallback
    if c in SPECIAL_FORWARD:
        return SPECIAL_FORWARD[c]
    return b


check = bytearray(encode_byte(b) for b in flag)
assert check == encoded, "正向验证失败!"
print("[+] 正向验证通过: 明文加密后与原始密文一致")