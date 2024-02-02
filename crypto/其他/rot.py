import hashlib
#https://buuoj.cn/challenges#rot

def rot():#将acii码数组转成文字
    str = '83 89 78 84 45 86 96 45 115 121 110 116 136 132 132 132 108 128 117 118 134 110 123 111 110 127 108 112 124 122 108 118 128 108 131 114 127 134 108 116 124 124 113 108 76 76 76 76 138 23 90 81 66 71 64 69 114 65 112 64 66 63 69 61 70 114 62 66 61 62 69 67 70 63 61 110 110 112 64 68 62 70 61 112 111 112'
    list = str.split(' ')
    print(list)
    flag = ''
    for each in list:
        flag += chr(int(each) - 13)
    print(flag)
    return flag


if __name__ == '__main__':
    flag_with_xx = rot()#文字flag中有未知字符，但是有md5值，穷举未知字符得出flag
    md5 = '38e4c352809e150186920aac37190cbc'
    for x1 in range(32, 123):
        for x2 in range(32, 123):
            for x3 in range(32, 123):
                for x4 in range(32, 123):
                    flag_new = 'flag{www_shiyanbar_com_is_very_good_' + chr(x1) + chr(x2)+ chr(x3) +chr(x4) + '}'
                    str1 = hashlib.md5(flag_new.encode('utf-8')).hexdigest()
                    if str1 == md5:
                        print(flag_new)
                        break
    print('no flag')
