import os
import pandas as pd
"""
对绿盟漏扫设备输出的主机扫描结果进行处理，找出所有扫描出开发的端口，整理在一个excel中
"""
df = pd.DataFrame([])


def find_skip_row(file):
    try:
        xls = pd.read_excel(file, sheet_name="其它信息", header=None)
    except Exception as e:
        print(f"{file} has no data: {e}")
        return None
    else:
        if xls.empty:
            print(f"{file} has no data: empty")
            return None
        target_value = '远程端口信息'
        skiprows = xls.index[xls.iloc[:, 0] == target_value]
        if skiprows.empty:
            print(f"{file} has no target value: {target_value}")
            return None
        skiprows = skiprows.item()
        xls = xls.iloc[skiprows + 2:]  # 跳过前面不要的行
        xls = xls.iloc[:, 1:-1]  # 删除第一列和最后一列开放状态
        first_empty_row = xls.apply(lambda row: row.isna().all(), axis=1).idxmax()  # 上面做完之后，找到第一个全为空的行，截断，就只剩下端口数据了
        if pd.notna(first_empty_row) and first_empty_row > 0:
            xls = xls.iloc[:(first_empty_row - skiprows - 2)]  # 索引在xls.iloc[skiprows+2:]之后没有变，所以要多减
    return xls


# 先将文件写入一个列表，稍后再处理
excel_files = [file for file in os.listdir(".") if file.endswith('.xlsx') or file.endswith('.xls')]

for file in excel_files:
    print(file + '_____')
    try:
        xls = find_skip_row(file)
        if xls is not None:
            xls = xls.assign(ip=file[:-4])#加入ip信息
            df = pd.concat([df, xls], ignore_index=True)
    except ValueError as e:
        print(f"Error processing file {file}: {e}")
        continue

df = df.rename(columns={1: '端口', 2: '协议', 3: '服务'})
print(df)
df.to_excel('端口统计.xlsx', index=False)
