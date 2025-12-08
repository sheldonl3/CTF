# https://blog.csdn.net/qq_36152465/article/details/128870293
#攻防世界  需要先与0x22
# RC4加密
def rc4(key, ciphertext):
    # 初始化S盒
    sbox = list(range(256))
    j = 0
    for i in range(256):
        j = (j + sbox[i] + key[i % len(key)]) % 256
        sbox[i], sbox[j] = sbox[j], sbox[i]

    # 生成密钥流
    i = 0
    j = 0
    flag = []
    for k in range(len(ciphertext)):
        i = (i + 1) % 256
        j = (j + sbox[i]) % 256
        sbox[i], sbox[j] = sbox[j], sbox[i]

        index = (sbox[i] + sbox[j]) % 256
        tmp = sbox[index]
        flag.append(tmp ^ ciphertext[k])

    # 将明文转换为字符串
    return ''.join([chr(p) for p in flag])


# 测试
key = b"12345678abcdefghijklmnopqrspxyz"
ciphertext = [0x9E, 0xE7, 0x30, 0x5F, 0xA7, 0x01, 0xA6, 0x53, 0x59, 0x1B, 0x0A, 0x20, 0xF1, 0x73, 0xD1, 0x0E, 0xAB,
              0x09, 0x84, 0x0E, 0x8D, 0x2B, 0x00, 0x00]

for i in range(len(ciphertext)):
    ciphertext[i] = ciphertext[i] ^ 0x22

plaintext = rc4(key, ciphertext)
print(plaintext)
