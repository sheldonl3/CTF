import os
import pandas as pd

df = pd.DataFrame([])
df.to_excel(r'端口统计.xlsx')

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

        # 查找第一个全为空值的行（包括索引为0的标题行）
        first_empty_row = xls.iloc[0:].apply(lambda row: row.isna().all(), axis=1).idxmax()
        # 如果找到了全为空值的行，则删除该行及其之后的所有行
        if pd.notna(first_empty_row):
            xls = xls.iloc[:first_empty_row]
        xls = xls.assign(ip=file[:-4])
        df = df._append(xls[0:])
print(df)
df.to_excel('端口统计.xlsx', index=False)

