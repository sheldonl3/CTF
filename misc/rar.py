import rarfile

flag = ''
rarf = rarfile.RarFile("48.rar")
'''
读取rar里面文件的修改时间01-21、01-33.。。。。。，转化为ascii
'''
for i in range(18):
    name = f'48/.{i}.txt'
    data = rarf.getinfo(name).date_time
    # print(data)
    time = data[-2] * 60 + data[-1]#分+秒
    # print(time)
    flag += chr(time)
print(flag)
