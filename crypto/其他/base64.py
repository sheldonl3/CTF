import base64
import string
str1='FlZNfnF6Qol6e9w17WwQQoGYBQCgIkGTa9w3IQKw'
string1='JKLMNOxyUVzABCDEFGH789PQIabcdefghijklmWXYZ0123456RSTnopqrstuvw+/'
string2='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
print(base64.b64decode(str1.translate(str.maketrans(string1,string2))))
#https://buuoj.cn/challenges#[BJDCTF2020]%E8%BF%99%E6%98%AFbase??
#base64的编码表换成题目要求的，再进行解码