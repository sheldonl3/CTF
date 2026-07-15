import base64
s = "you_know_how_to_remove_junk_code"
f = ''
for i in s:
    f += chr(ord(i) ^ 0x25)
print(f)
print(base64.b64encode(f.encode()))