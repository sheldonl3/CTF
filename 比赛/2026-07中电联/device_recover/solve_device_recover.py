#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
device_recover 解密脚本（仅解密 flag）
reveal_flag 中硬编码的 5 个 8 字节常量，按小端展开到连续缓冲，
第 5 个写在偏移 30（与第 4 个重叠 2 字节），整体 XOR 0x4c 得 flag。
"""

# reveal_flag 里的 5 个 movabs 常量 + 写入偏移（相对 buffer 起点 rbp-0x30）
CONSTS = [
    (0x30206372b2d202a, 0),
    (0x1d2e257e070b3e0e, 8),
    (0x3e7e2b1d7a342904, 16),
    (0x2781b2a3c1b792e, 24), #第 4 个和第 5 个常量的重叠,
    (0x31271c7b36190278, 30),#先写 q3(占 24–31),再写 q4(占 30–37),q4 的切片赋值自然把 30、31 两个位置覆盖掉
]
XOR_KEY = 0x4c
FLAG_LEN = 38

def decode_flag():
    buf = bytearray(64)
    for val, off in CONSTS:
        buf[off:off + 8] = (val & 0xFFFFFFFFFFFFFFFF).to_bytes(8, 'little')#转换为小端序列
        print(buf.hex())
    return bytes(b ^ XOR_KEY for b in buf[:FLAG_LEN])


if __name__ == '__main__':
    flag = decode_flag()
    print(flag)
