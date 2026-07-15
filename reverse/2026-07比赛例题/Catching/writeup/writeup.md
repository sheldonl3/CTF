# Catching

题目用C++编写，简单算法rot13，其中大写字母会触发整数异常，执行异常catch逻辑，catch逻辑为向右偏移5，后异或0x4f，最后和checkflag数据作比较，由于使用C++的string类型，反编译结果会比较抽象。需要调试理解。

## 加密逻辑

输入字符串，小写字母进行rot13，大写字母进行rot13后触发异常进行rot5、异或0x4f，接着`{``}`会被随机替换成9和6，`_`会被随机替换成`#`，`!`会被随机替换成`*`,如果不是大小写或`{`、`}`、`_`、`!`,则不变。
逆向推回去即可。
```c++
string rot13(string str) {
	int a = 0;
	for (int i = 0; i < str.length(); i++) {
		if (islower(str[i])) {
			str[i] -= 'a';
			str[i] = (str[i] + 13) % 26 + 'a';
		}
		else if (isupper(str[i])) {
			try
			{
				str[i] -= 'A';
				str[i] = (str[i] + 13) % 26 + 'A';
				throw 0;
			}
			catch (int& a)
			{
				str[i] = (str[i] - 'A' + 5) % 26 + 'A';
				str[i] ^= 0x4f;
			}

		}
		else if (str[i] == '}') {
			str[i] = '6';
		}
		else if (str[i] == '{') {
			str[i] = '9';
		}
		else if (str[i] == '_') {
			str[i] = '#';
		}
		else if (str[i] == '!') {
			str[i] = '*';
		}
	}
	return str;
}
```
## exp
```python
strr = [0x73,0x79,0x6e,0x74,0x39,0x09,0x76,0x70,0x72,0x23,0x17,0x79,0x6e,0x74,0x23,0x76,0x66,0x23,0x75,0x72,0x65,0x72,0x23,0x1c,0x65,0x72,0x23,0x6c,0x62,0x68,0x17,0x76,0x61,0x71,0x2a,0x2a,0x2a,0x36]
flag= ''
mark = 0
for i in range(38):
    if strr[i]>=97 and strr[i]<=122:
        #print(i)
        flag += chr(((strr[i] - 97 + 13) % 26) + 97)
    elif strr[i]^0x4f>=65 and strr[i]^0x4f<=90:
        tmp = strr[i]^0x4f
        #print(tmp,i)
        tmp = ((tmp - 65  - 5) % 26) + 65
        tmp = ((tmp - 65  + 13) % 26) + 65
        flag += chr(tmp)
    elif strr[i]==35 :
        flag += '_'
    elif strr[i]== 42 :
        flag += '!'
    elif strr[i]==54:
        flag += '}'
    elif strr[i]==57:
        flag += '{'       
    else:
        flag += chr(strr[i])
print(flag)
#flag{Nice_Flag_is_here_Are_youFind!!!}

```
