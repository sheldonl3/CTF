import os

import pandas as pd

df = pd.DataFrame([])
df.to_excel(r'端口统计.xlsx')


# 查找跳过多少行才是端口数据
def find_skip_row(file):
    skiprows = 0
    try:
        xls = pd.read_excel(file, sheet_name="其它信息", header=None)
    except Exception as e:  # 使用具体的异常类型可能更好，但这里为了简单起见使用Exception
        print(f"v1 {file} has no data: {e}")
    else:
        if xls.empty:
            print(file + "v2 has no data:empty")
        target_value = '远程端口信息'
        skiprows = xls.index[xls.iloc[:, 0] == target_value].item()
        print('skiprows is ' + str(skiprows))
    return skiprows


# 先将文件写入一个列表，稍后再处理
excel_files = []
for file in os.listdir("."):
    if file.endswith('.xlsx') or file.endswith('.xls'):  # 确保文件是Excel格式
        excel_files.append(file)

for file in excel_files:
    print(file + '_____')
    try:
        xls = pd.read_excel(file, sheet_name="其它信息", header=1, usecols=['端口', '协议', '服务'],
                            skiprows=find_skip_row(file))
    except Exception as e:  # 使用具体的异常类型可能更好，但这里为了简单起见使用Exception
        print(f"{file} has no data: {e}")
        continue
    else:
        if xls.empty:
            print(file + " has no data:empty")
            continue

        # 查找第一个全为空值的行（包括索引为0的标题行）
        first_empty_row = xls.iloc[0:].apply(lambda row: row.isna().all(), axis=1).idxmax()
        # 如果找到了全为空值的行，则删除该行及其之后的所有行
        if pd.notna(first_empty_row):
            xls = xls.iloc[:first_empty_row]
        xls = xls.assign(ip=file[:-4])
        df = pd.concat([df, xls], ignore_index=True)

print(df)
df.to_excel('端口统计.xlsx', index=False)
