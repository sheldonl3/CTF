# import gmpy2
# from Crypto.Util.number import *
# from flag import flag
# m = bytes_to_long(flag.encode())
# e = 65537
# p = getPrime(512)
# q = getPrime(512)
# n = p*q 
# c = pow(m,e,n)
# dp = inverse(e, (p-1))
# dq = inverse(e, (q-1))
# m1 = pow(c,dp, p)
# m2 = pow(c,dq, q)
# q_inv = inverse(q, p)
# h = (q_inv*(m1-m2)) % p
# print('m2 =', m2)
# print('h =', h)
# print('q =', q)
# #


import gmpy2
from Crypto.Util.number import long_to_bytes
m2 = 5273633697263204052874375863961685651561232937704513453247123197363319135890690087842300598445444689808150366073992720370685169830835927736165228555213013
h = 14384629843882054286212724866634561127995147703201269293846355523736
q = 8176230364620937806108907974516734557941468404958237659416103599132889245787418021102295877976148147030502703221686671065350510491649581178217052988807607


# 计算 m = m2 + q * h
m = m2 + q * h
print("m =", m)

# 转为 flag
flag = long_to_bytes(m)
print("Flag:", flag)

#flag{crt_1s_fun}