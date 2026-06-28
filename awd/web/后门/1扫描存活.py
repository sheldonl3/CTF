import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging
from awd.config import ownip_c

# from requests.packages.urllib3.exceptions import InsecureRequestWarning

# 配置参数
IP_RANGE = range(0, 255)
PORTS = [8801,8802,8803,8804,8805]  # 可扩展常见Web端口
TIMEOUT = 3
THREADS = 20
# 精确屏蔽 InsecureRequestWarning 警告
# requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def process_host():  # 探活

    """并发探活，返回可达IP列表"""
    live_ips = []
    #base_ips = [f"192.168.{i}.2" for i in IP_RANGE if i !=ownip_c]
    base_ips = [f"156.239.238.67"]
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
    with open("ip.txt", "w", encoding="utf-8") as f:
        for ip in live_ips:
            f.write(ip + "\n")
    return live_ips


if __name__ == "__main__":
    process_host()
