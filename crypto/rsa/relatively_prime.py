# import gmpy2
# import random   
# from Crypto.Util.number import *
# import libnum
# from flag import flag
# m=bytes_to_long(flag.encode())
# while 1:
#     e=random.randint(100,1000)
#     p=getPrime(1024)
#     q=getPrime(1024)
#     t=gmpy2.gcd(e,(p-1)*(q-1))
#     if gmpy2.invert(e//t,(p-1)*(q-1))and t != 1:
#         break
# n=p*q
# c=pow(m,e,n)
# print("q=",q)
# print("p=",p)
# print("c=",c)
# print("e=",e)



import gmpy2

from Crypto.Util.number import long_to_bytes



def mod_root_prime(a, t, p):
    """解 x^t ≡ a mod p，返回所有解（列表）"""
    if a % p == 0:
        return [0]
    # 找到原根（这里简单用 g=2 尝试）
    g = 2
    while pow(g, (p-1)//2, p) == 1:
        g += 1
    # 解离散对数：g^e ≡ a mod p
    # 由于 p 很大，这里用 Pohlig-Hellman 简化（但 t 小，可以直接枚举）
    # 更简单的方法：如果 gcd(t, p-1)=1，则直接 pow(a, invert(t, p-1), p)
    # 否则需要处理多个解
    g = 2
    # 这里用简单方法：如果 t | (p-1) 且 a^{(p-1)/t} ≡ 1 mod p，则有解
    # 实际上可以用以下方法：
    # 令 d = gcd(t, p-1)
    # 方程有解当且仅当 a^{(p-1)/d} ≡ 1 mod p
    # 解的个数为 d
    # 这里我们直接用 gmpy2 的 nthroot_mod（如果可用）
    try:
        # gmpy2 的 powmod 加搜索
        # 简单方法：枚举
        solutions = []
        for x in range(p):
            if pow(x, t, p) == a % p:
                solutions.append(x)
        return solutions
    except:
        pass
    # 更高效的方法：利用原根和离散对数
    # 但此处 t 小，可以直接用下面方法
    return []

q= 100642814467179968207588991041227075062900797001253228676632499249148804472025260926110323727836593174154842790742750873022959061505581706428013859566184339522857489129255264017220442161098637879787083565775092047190728232297216677543381055273547299874725938596652726845571226212528837804177826485959292016447
p= 92153322628568256031390818827073089074700772508769536983118498335948999919717886598746077250758917396118278221948111149486605270006044269819202506432405257383826912467965002147543248661538770111581000008035421830939050386341801079517096142139799128176859637096885263323329806891793937133012476623509113100777
c= 6480380377586927065930685869815665997834367301473183971624579980549089996614206469552194085967210619902806642283348698102484704270263972150030156630112263374503491957980524431584845679517771030081292028140451249798487407640598157758755837680768754871628326381847324167242833399568269614324613329857233488114021057860475385513569780949879692875913587062011085100796541747329401852918128072612694266231612247522173905401492163748032181266787561255570246525249182898174731203841336257532952566674061230699341210749861202869389964138147650051617395140762461764490954255318421632205083163907693943828011092993116674332684
e= 400


n = p * q
phi = (p-1) * (q-1)

t = gmpy2.gcd(e, phi)
print(f"t = {t}")

e_prime = e // t
d_prime = gmpy2.invert(e_prime, phi)

m_t = pow(c, d_prime, n)
print(f"m^t = {m_t}")

root, exact = gmpy2.iroot(m_t, t)
if exact:
    print("Exact integer root found.")
    m = root
    flag = long_to_bytes(m)
    print(f"Flag: {flag}")
else:
    print("ssss")
    # 分别在模 p 和模 q 下求解
    sols_p = mod_root_prime(m_t, t, p)
    sols_q = mod_root_prime(m_t, t, q)
    print(f"Solutions mod p: {len(sols_p)}")
    print(f"Solutions mod q: {len(sols_q)}")
    
    # 用 CRT 组合所有解
    possible_ms = []
    for xp in sols_p:
        for xq in sols_q:
            m_crt = int(gmpy2.crt([p, q], [xp, xq])[0])
            possible_ms.append(m_crt)
    
    # 逐个尝试解码
    for m_candidate in possible_ms:
        flag_candidate = long_to_bytes(m_candidate)
        print(flag_candidate)
        if b'flag{' in flag_candidate:
            print(f"Found flag: {flag_candidate}")
            break


        b'flag{400_8_50}'