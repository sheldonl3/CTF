import pythonping
from concurrent.futures import ThreadPoolExecutor
import os
from awd.config import ownip_c


def get_ip(ip):
    res = pythonping.ping(ip)
    print(ip)
    if "Reply" in str(res):
        print(ip + " 是存活地址")
        with open("ip.txt", 'a', encoding='UTF-8') as f:
            f.write(f"{ip}\n")


ip = []
if os.path.exists("ip.txt"):
    os.remove("ip.txt")
for num in range(1, 255): #多道题的靶机
    if num!=ownip_c:
        ip.append("192.168." + str(num) + ".2")
with ThreadPoolExecutor(max_workers=100) as executor:
    result = executor.map(get_ip, ip)
