musical_notation = [111, 114, 157, 166, 145, 123, 145, 143, 165, 162, 151, 164, 171, 126, 145, 162, 171, 115, 165, 143, 150]
flag="flag{"
for i in musical_notation:
    flag+=chr(int(str(i),8))
flag+="}"
print(flag)

#https://buuoj.cn/challenges#%E5%AF%86%E7%A0%81%E5%AD%A6%E7%9A%84%E5%BF%83%E5%A3%B0
#密码学的心声：将乐谱的3位数子看成一个ascii码，转换成char