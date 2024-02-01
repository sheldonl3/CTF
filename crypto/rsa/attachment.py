import gmpy2
import binascii

#https://buuoj.cn/challenges#[HDCTF2019]basic%20rsa
flag = "*****************"

p = 262248800182277040650192055439906580479
q = 262854994239322828547925595487519915551

e = 65533
n = p*q
'''
c = pow(int(b2a_hex(flag.encode()),16),e,n)

print(c)
'''
c= 27565231154623519221597938803435789010285480123476977081867877272451638645710
phi = (p-1)*(q-1)
d = gmpy2.invert(e,phi)
m = gmpy2.powmod(c,d,p*q)

print(binascii.unhexlify(hex(m)[2:]))#十进制与字节互相转换(mac方法)