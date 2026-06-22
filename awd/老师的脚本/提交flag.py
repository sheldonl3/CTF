import requests
import time

# 将 [token] 替换为您的实际 token
token = "a4c0231a8634a1dd45c10c2d487693fb"

# API 端点
api_url = "http://156.239.238.67:19999/#/flag"

flags=[]
# 读取 flag.txt 文件
with open("./自动_flag.txt", "r") as file:
    for line in file:
        line = line.strip()  # 去除行首尾的空白字符和换行符
        if line:  # 确保不是空行
            key, value = line.split(":", 1)  # 使用 maxsplit=1 防止值中包含冒号被错误分割
            print(value)
            url,flag = value.split(":", 1)
            flags.append(flag)
# 循环提交 flag
for flag in flags:
    # 去除 flag 开头和结尾的空白字符
    flag = flag.strip()

    # 准备要发送的请求数据
    data = {"token": token, "flag": flag}

    # 发送 POST 请求提交 flag
    response = requests.post(api_url, data=data)

    # 打印响应内容
    print(f"提交的 flag: {flag}")
    print(f"响应内容: {response.text}")

    # 等待几秒钟再进行下一次提交
    time.sleep(1)
