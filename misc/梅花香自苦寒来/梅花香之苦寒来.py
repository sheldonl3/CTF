with open('梅花.txt', 'r') as res:  # 坐标格式文件比如(7,7)
    re = res.read()
    res.close()

with open('output.txt', 'w') as gnup:  # 将转换后的坐标写入gnuplotTxt.txt
    re = re.split()
    tem = ''
    for i in range(0, len(re)):
        tem = re[i]
        tem = tem.lstrip('(')
        tem = tem.rstrip(')')
        for j in range(0, len(tem)):
            if tem[j] == ',':
                tem = tem[:j] + ' ' + tem[j + 1:]
        gnup.write(tem + '\n')
    gnup.close()