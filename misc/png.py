with open('download.png', 'rb') as f:
    data = f.read()
# 定位IEND块后的数据起始位置
iend_pos = data.find(b'IEND') + 8
hidden_data = data[iend_pos:]
with open('提取结果.bin', 'wb') as out:
    out.write(hidden_data)
