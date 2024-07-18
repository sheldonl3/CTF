import os

import pandas as pd

# df=pd.DataFrame([])
# df.to_excel(r'C:\xxx\test1.xlsx')
dir = '/home/kali/Desktop/多任务输出_2024_07_09_内网常态xls/'
for file in os.listdir(dir):
    print(file)
    try:
        xls = pd.read_excel(dir+file, sheet_name="其它信息",header=1,usecols=['端口', '协议', '服务'])
    except:
            print(file + " has no data")
    else:
        if xls.empty:
            print(file + " has no data")
            continue
        print(file + " has data ")
        print(xls)  # 列名



