#!/usr/bin/env python3
# solve_dccore.py —— dccore 一键解法
import struct

CORE = r"D:/Study/培训-检查/20260610--北京公司培训/团队赛/dccore/dc.core"
BASE = 0x55c62414e000  # 主模块加载基址

def vaddr_to_off(data, v):
    """ELF PT_LOAD 段: vaddr -> file offset 映射"""
    e_phoff = struct.unpack_from("<Q", data, 0x20)[0]
    e_phentsz = struct.unpack_from("<H", data, 0x36)[0]
    e_phnum = struct.unpack_from("<H", data, 0x38)[0]
    for i in range(e_phnum):
        off = e_phoff + i * e_phentsz
        if struct.unpack_from("<I", data, off)[0] != 1:  # PT_LOAD
            continue
        p_offset = struct.unpack_from("<Q", data, off + 8)[0]
        p_vaddr  = struct.unpack_from("<Q", data, off + 16)[0]
        p_filesz = struct.unpack_from("<Q", data, off + 32)[0]
        if p_vaddr <= v < p_vaddr + p_filesz:
            return p_offset + (v - p_vaddr)
    raise ValueError(f"vaddr {v:#x} not in any PT_LOAD segment")

data = open(CORE, "rb").read()

# 1) 直接从 core 提取三个缓冲区的原始字节
raw_KEY = data[vaddr_to_off(data, BASE + 0x4020):][:14]
raw_TAB = data[vaddr_to_off(data, BASE + 0x4040):][:64]
raw_TGT = data[vaddr_to_off(data, BASE + 0x40a0):][:52]

# 2) init wrapper 的 XOR 解码
KEY = bytes(b ^ 0x56 for b in raw_KEY)   # -> C0nFu5i0n_K3y!
TAB = bytes(b ^ 0x42 for b in raw_TAB)   # 64 字符自定义字母表
TGT = bytes(b ^ 0x24 for b in raw_TGT)   # 程序中 strcmp 比对的目标串
assert len(set(TAB)) == 64

# 3) 篡改版 RC4（逐条反汇编 core 二进制确认）
def mod_rc4(buf, key):
    S = list(range(256))
    j = 0
    for i in range(256):                       # KSA: 比标准多一个 +i
        j = (j + S[i] + key[i % len(key)] + i) & 0xff
        S[i], S[j] = S[j], S[i]
    out = bytearray()
    i = j = 0
    for k in range(len(buf)):                 # PRGA
        i = (i + 1) & 0xff
        j = (j + S[i]) & 0xff
        S[i], S[j] = S[j], S[i]
        # 关键: 把输出字节位置 k 异或进密钥流; 用 S[i]+S[j] 之和(非标准 S[sum])
        ks = (k ^ ((S[i] + S[j]) & 0xff)) & 0xff
        out.append(buf[k] ^ ks)
    return bytes(out)

# 4) 位置相关的自定义 base64
def b64_decode(s, tab):
    s = s.rstrip(b"\x00")
    out = bytearray()
    pos = 0
    while pos + 4 <= len(s):
        idxs = [(tab.index(s[pos + t]) - ((pos + t) % 7) - 3) % 64 for t in range(4)]
        i0, i1, i2, i3 = idxs
        out += bytes([(i0 << 2) | (i1 >> 4),
                      ((i1 & 0xf) << 4) | (i2 >> 2),
                      ((i2 & 0x3) << 6) | i3])
        pos += 4
    return bytes(out)

def b64_encode(buf, tab):
    out = bytearray()
    op = 0                      # 累计输出位置 (0,1,2,3,...)
    for p in range(0, len(buf), 3):
        b0, b1, b2 = buf[p], buf[p + 1], buf[p + 2]
        i0 = b0 >> 2
        i1 = ((b0 << 4) & 0x30) | (b1 >> 4)
        i2 = ((b1 << 2) & 0x3c) | (b2 >> 6)
        i3 = b2 & 0x3f
        for idx in (i0, i1, i2, i3):
            out.append(tab[(idx + (op % 7) + 3) % 64])
            op += 1
    return bytes(out)

# 5) 还原 flag: TGT = b64(RC4(flag))  =>  flag = RC4(b64_decode(TGT))
cipher = b64_decode(TGT, TAB)
flag = mod_rc4(cipher, KEY)

# 6) 正反验证, 确认不是巧合: TGT 应当等于 b64(RC4(flag))
assert b64_encode(mod_rc4(flag, KEY), TAB) == TGT

print("KEY   :", KEY)
print("TGT   :", TGT)
print("cipher:", cipher.hex(), f"({len(cipher)} bytes)")
print("FLAG  :", flag.decode())
assert flag.startswith(b"flag{") and flag.endswith(b"}")
print("\n>>> FLAG =", flag.decode())