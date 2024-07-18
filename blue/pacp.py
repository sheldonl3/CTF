import re
#处理抓包之后的数据文件，找出布尔注入的flag

f = open('ttest.txt', 'r')
lines = f.readlines()

flag_dic = {}

for line in lines:
    match_obj = re.search(r'from db_flag.tb_flag  limit 0,1\)\),(.*?), 1\)\)>(.*?) HTTP/(.*?).1', line)
    #from db_flag.tb_flag  limit 0,1)), 3, 1))>50 HTTP/1.1   把需要提取的内容替换成(.*?)
    if match_obj:
        key = int(match_obj.group(1))
        value = int(match_obj.group(2))
        flag_dic[key] = value
print(flag_dic)
flag = ''
for value in flag_dic.values():
    flag += chr(value)
print(flag)
