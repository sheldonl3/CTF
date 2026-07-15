import pythonping
from concurrent.futures import ThreadPoolExecutor
import os
from awd.config import ownip_c

timudiz = "5" #改成自己靶机的最后一位地址


def get_ip(ip):
    ping = pythonping.ping(ip)
    print(ip)
    if "Reply" in str(ping):
        print(ip + " 是存活地址")
        res.append(ip)


ip = []
res = []
if os.path.exists("ip.txt"):
    os.remove("ip.txt")
for num in range(1, 255):  # 多道题的靶机
    if num != ownip_c:
        ip.append("172.30." + str(num) +'.'+timudiz)
with ThreadPoolExecutor(max_workers=100) as executor:
    result = executor.map(get_ip, ip)
if res:
    with open("ip.txt", 'a', encoding='UTF-8') as f:
        for each in res:
            #f.write(f"http://{each}/\n")
            f.write(f"{each}\n")
