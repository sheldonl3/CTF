import base64
 
Des="e3nifIH9b_C@n@dH"
flag=""
 
for i in range(len(Des)):
    flag+=chr(ord(Des[i])-i)
print(flag)
print(base64.b64decode(flag))