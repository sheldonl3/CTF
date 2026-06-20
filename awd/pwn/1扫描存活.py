import socket
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging

# 配置参数
IP_RANGE = range(0, 255)
PORTS = 1337  # 可扩展常见Web端口
TIMEOUT = 3
THREADS = 20
# 精确屏蔽 InsecureRequestWarning 警告
# requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def process_host():  # 探活

    """并发探活，返回可达IP列表"""
    live_ips = []
    base_ips = [f"192.168.{i}.3" for i in IP_RANGE]

    def scan_host(ip):
        """扫描单个主机是否开放PWN端口"""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(1)
                result = sock.connect_ex((str(ip), PORTS))
                if result == 0:
                    logging.info(f"{ip}:{PORTS} alive")
                    return ip
                else:
                    logging.info(f"{ip}:{PORTS} not alive")
        except Exception as e:
            print(e)
        return None

    with ThreadPoolExecutor(max_workers=THREADS) as executor:
        futures = {executor.submit(scan_host, ip): ip for ip in base_ips}
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
