import re

# 密文（checkflag）的十六进制数据
hex_data = (
    "0x73, 0x79, 0x6e, 0x74, 0x39, 0x9, 0x76, 0x70, 0x72, 0x23, 0x17, "
    "0x79, 0x6e, 0x74, 0x23, 0x76, 0x66, 0x23, 0x75, 0x72, 0x65, 0x72, "
    "0x23, 0x1c, 0x65, 0x72, 0x23, 0x6c, 0x62, 0x68, 0x17, 0x76, 0x61, "
    "0x71, 0x2a, 0x2a, 0x2a, 0x36"
)

# 解析为字节列表
cipher_bytes = [int(x, 16) for x in re.findall(r'0x[0-9a-fA-F]+', hex_data)]

def decrypt_byte(b: int) -> str:
    """逆向 rot13 变体（解密）"""
    ch = chr(b)
    # 特殊符号反向映射
    if ch == '6':
        return '}'
    elif ch == '9':
        return '{'
    elif ch == '#':
        return '_'
    elif ch == '*':
        return '!'
    # 字母 ROT13（自反）
    elif 'a' <= ch <= 'z':
        return chr((ord(ch) - ord('a') + 13) % 26 + ord('a'))
    elif 'A' <= ch <= 'Z':
        return chr((ord(ch) - ord('A') + 13) % 26 + ord('A'))
    else:
        return ch   # 其他字符原样保留

# 解密并拼接
flag = ''.join(decrypt_byte(b) for b in cipher_bytes)

print("正确的 flag 为：")
print(flag)
print("\n转义表示（含不可见字符）：")
print(repr(flag))
