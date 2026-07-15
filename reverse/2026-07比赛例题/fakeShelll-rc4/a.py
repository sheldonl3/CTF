import struct

def rc4_crypt(data: bytes, key: bytes) -> bytes:
    S = list(range(256))
    j = 0
    for i in range(256):
        j = (j + S[i] + key[i % len(key)]) % 256
        S[i], S[j] = S[j], S[i]
    i = j = 0
    out = []
    for byte in data:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        out.append(byte ^ S[(S[i] + S[j]) % 256])
    return bytes(out)
    
'''
# 原始数据（4个64位整数）
v7 = [
    0xE0B25F3D8FFA94B6,
    0xE79D6C9866D20FEA,
    0x6D6FBEC57140081B,
    0xF6F3BDA88D097B7C
]

# 关键：使用 '<Q' 表示小端序无符号长整型打包
data = b''.join(struct.pack('<Q', val) for val in v7)

# 解密（RC4加密解密算法相同）
result = rc4_crypt(data, b"happyhg4me!")

print("Hex结果:", result.hex())
# 尝试打印为字符串（如果结果是可读文本）
try:
    print("明文:", result.decode('utf-8'))
except UnicodeDecodeError:
    print("结果为二进制数据，无法直接UTF-8解码")
'''


hex_str = "E0B25F3D8FFA94B6E79D6C9866D20FEA6D6FBEC57140081BF6F3BDA88D097B7C"
data = bytes.fromhex(hex_str)
result = rc4_crypt(data, b"happyhg4me!")
print(result.hex())
