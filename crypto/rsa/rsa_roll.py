import gmpy2
from Cryptodome.Util.number import long_to_bytes

#https://buuoj.cn/challenges#RSAROLL

e = 19
n = 920139713
p = 18443  #在线解密网站解出pq
q = 49891
list_c = [704796792,
          752211152,
          274704164,
          18414022,
          368270835,
          483295235,
          263072905,
          459788476,
          483295235,
          459788476,
          663551792,
          475206804,
          459788476,
          428313374,
          475206804,
          459788476,
          425392137,
          704796792,
          458265677,
          341524652,
          483295235,
          534149509,
          425392137,
          428313374,
          425392137,
          341524652,
          458265677,
          263072905,
          483295235,
          828509797,
          341524652,
          425392137,
          475206804,
          428313374,
          483295235,
          475206804,
          459788476,
          306220148]

flag = ''
phin = (q - 1) * (p - 1)
d = gmpy2.invert(e, phin)

for each in list_c:
    m = gmpy2.powmod(each, d, p * q)
    flag += long_to_bytes(m).decode()
print(flag)
