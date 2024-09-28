'''
[ACTF新生赛2020]base64隐写
直接修改读取的文件，运行脚本
'''
base64 = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
binstr=""
strings = open('./ComeOn!.txt').read()
e = strings.splitlines()
for i in e:
    if i.find("==") > 0:
        temp = bin((base64.find(i[-3]) & 15))[2:]
        # 取倒数第3个字符，在base64找到对应的索引数（就是编码数），取低4位，再转换为二进制字符
        binstr = binstr + "0" * (4 - len(temp)) + temp  # 二进制字符补高位0后，连接字符到binstr
    elif i.find("=") > 0:
        temp = bin((base64.find(i[-2]) & 3))[2:]  # 取倒数第2个字符，在base64找到对应的索引数（就是编码数），取低2位，再转换为二进制字符
        binstr = binstr + "0" * (2 - len(temp)) + temp  # 二进制字符补高位0后，连接字符到binstr
str = ""
for i in range(0, len(binstr), 8):
    str = str + chr(int(binstr[i:i + 8], 2))  # 从左到右，每取8位转换为ascii字符，连接字符到字符串
print(str)