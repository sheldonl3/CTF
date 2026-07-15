# s2 = "30074D214E235B73612A5030547B3F767C05472D5E612A5054635B256A4A1D44"  #有多余的数据612a50，需要删掉
s2 = "30074D214E235B7330547B3F767C05472D5E612A5054635B256A4A1D44"#密文按双字节为一段，进行反转（剔除多余内容）

data_correct = b''

for i in range(0, len(s2), 16):
    chunk = bytes.fromhex(s2[i:i + 16])
    print(chunk.hex())
    data_correct += chunk[::-1]

# 密文十六进制字符串
print(data_correct.hex())
data = "735b234e214d0730763f7b5430502a615e2d47057c441d4a6a255b6354"#反转结果
print(data)
# 转换为字节串
ciper = bytes.fromhex(data)
print(ciper)
# 密钥 (5字节循环)
key = [0x15, 0x37, 0x42, 0x29, 0x5A]

# 解密
flag = bytearray()
for i in range(len(ciper)):
    flag.append(ciper[i] ^ key[i % len(key)])

# 输出结果
print(flag.decode())
