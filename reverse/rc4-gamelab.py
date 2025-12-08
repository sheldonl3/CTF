#https:// blog.csdn.net / yjh_fnu_ltn / article / details / 138248458
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
    keystream = []
    for _ in range(len(ciphertext)):
        i = (i + 1) % 256
        j = (j + sbox[i]) % 256
        sbox[i], sbox[j] = sbox[j], sbox[i]
        k = sbox[(sbox[i] + sbox[j]) % 256]
        keystream.append(k)
    # print(keystream)

    # 解密密文
    plaintext = []
    for i in range(len(ciphertext)):
        m = ciphertext[i] ^ keystream[i]
        plaintext.append(m)
    print(plaintext)

    # 将明文转换为字符串
    return ''.join([chr(p) for p in plaintext])


# 测试
key = b"gamelab@"
ciphertext = [0xB6, 0x42, 0xB7, 0xFC, 0xF0, 0xA2, 0x5E, 0xA9, 0x3D, 0x29, 0x36, 0x1F, 0x54, 0x29,
              0x72, 0xA8, 0x63, 0x32, 0xF2, 0x44, 0x8B, 0x85, 0xEC, 0xD, 0xAD, 0x3F, 0x93, 0xA3, 0x92,
              0x74, 0x81, 0x65, 0x69, 0xEC, 0xE4, 0x39, 0x85, 0xA9, 0xCA, 0xAF, 0xB2, 0xC6]
# for i in ciphertext:
#     print(chr(i),end="")
plaintext = rc4(key, ciphertext)
print(plaintext)
# flag{12601b2b-2f1e-468a-ae43-92391ff76ef3}
