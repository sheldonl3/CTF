flagtrue = "dd2940c04462b4dd7c450528835cca15"
x = []
for each in flagtrue:
    x.append(ord(each))
print(x)
ix = 2
x[ix] = (x[ix] + x[3]) - 50
x[4] = (x[ix] + x[5]) - 48
x[30] = (x[31] + x[9]) - 48
x[14] = (x[27] + x[28]) - 97
for i in range(16):
    ix1 = 31 - i
    a = x[ix1]
    ix1 = 31 - i
    x[ix1] = x[i]
    x[i] = a
print(x)
flag = ''
for each in x:
    flag += chr(each)

print(flag)
