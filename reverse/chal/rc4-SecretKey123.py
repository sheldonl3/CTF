#上课例题 
#def  s_box(key):
#     sbox=[0]*256
#     for i in range(0,256):
#       sbox[i] = i
#     v6=0
#     for i in range(0,256):
#       v6 = (ord(key [i%12]) + sbox[i] + v6) % 256
#       v1 = sbox[i]
#       sbox[i]=sbox[v6]
#       sbox[v6]=v1
#     return sbox

# def RC4(sbox,secrt,len):
#     v3 = 0
#     v4 = 0
#     res=[0]*len
#     for i in range(0,len):
#         v3 = (v3 + 1) % 256
#         v4 = (sbox[v3] + v4) % 256
#         #swap
#         linshi=sbox[v3]
#         sbox[v3]=sbox[v4]
#         sbox[v4]=linshi
#         secrt[i] ^= 0x21
#         res[i]=secrt[i]^sbox[(sbox[v4] + sbox[v3]) % 256]
#     return res

# if __name__ == "__main__":
#     enc=[0x2F,0xAA,0x99, 0x57, 0x90,0x83,0x3A,0xB7,0x57,0x9A,0x1B,0x60,0x53,0xE1,0xF9,0x9F
#         ,0x8,0x4D,0x35,0x43,0x99,0xBB]
#     str="SecretKey123"
#     sbox=s_box(str)
#     dec=RC4(sbox,enc,len(enc))
#     for i in range(len(enc)):
#         print(chr(dec[i]),end="")


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
        flag.append(0x21 ^ tmp ^ ciphertext[k])

    # 将明文转换为字符串
    return ''.join([chr(p) for p in flag])


# 测试
key=b"SecretKey123"
ciphertext = [0x2F,0xAA,0x99, 0x57, 0x90,0x83,0x3A,0xB7,0x57,0x9A,0x1B,0x60,0x53,0xE1,0xF9,0x9F
        ,0x8,0x4D,0x35,0x43,0x99,0xBB]

plaintext = rc4(key, ciphertext)
print(plaintext)

    
