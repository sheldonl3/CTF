'''
题目：梅花香之苦寒来
把坐标(7,11)转化为7 11格式
(7,11)->7 11
之后可以用gnuplot 画二维码
'''

with open('download.txt', 'r') as a:
    a = a.read()
    a = a.split()
    tem = ''
    f = open('plot.txt', 'w')
    for i in range(0, len(a)):
        tem = a[i]
        tem = tem.lstrip('(')
        tem = tem.rstrip(')')
        for j in range(0, len(tem)):
            if tem[j] == ',':
                tem = tem[:j] + ' ' + tem[j + 1:]
        print(tem, file=f)