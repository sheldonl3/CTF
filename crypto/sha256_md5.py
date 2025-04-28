import pandas as pd
import hashlib
'''计算xls第一列数据的hash值'''
def calculate_md5(text):
    """计算字符串的哈希值"""
    if pd.isna(text):  # 处理空值
        return None
    text = str(text)   # 强制转为字符串（兼容数字/日期等类型）
    return hashlib.md5(text.encode('utf-8')).hexdigest()
    #return hashlib.sha256(text.encode('utf-8')).hexdigest()

# 读取Excel文件
df = pd.read_excel('sha1.xlsx', engine='openpyxl')

# 对A列所有值计算MD5，结果存入新列
df['SHA'] = df['A'].apply(calculate_md5)

# 保存结果到新文件
df.to_excel('outputsha.xlsx', index=False, engine='openpyxl')
