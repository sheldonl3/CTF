import base64
'''
reverse_3
字符串base64加密之后，再加自己的下标
解密反向操作
'''
Des = "e3nifIH9b_C@n@dH"
flag = ""

for i in range(len(Des)):
    flag += chr(ord(Des[i]) - i)
print(flag)
print(base64.b64decode(flag))