'''
计算字符串的异或,绕过waf
比如_POST计算为
{'_': ('!', '~'), 'G': ('{', '<'), 'E': ('%', '`'), 'T': ('*', '~')}
在php中可以定义为
$_g =('!'^'~'). ('{'^'<').('%'^'`').('*'^'~');
'''
target = "_POST"
allowed = "!@#$%^&*()_+{}[]|\\:\"';<>?,./~`-="
result = {}
for c in target:
    for a in allowed:
        for b in allowed:
            if ord(a) ^ ord(b) == ord(c):
                result[c] = (a, b)
                break
        if c in result:
            break
print(result)