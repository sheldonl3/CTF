#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ecc-no CTF 完整解题脚本
========================
Level 1: ECC 但私钥 k 被直接打印泄露 -> 直接还原 m1
Level 2: 异常曲线 (anomalous, #E = p) 上的 ECDLP -> Smart's attack (纯 Python p-adic)

运行: python3 ecc.py
依赖: 仅标准库
"""
from math import gcd

# ======================================================================
# 题目公开数据 (来自 output 文件)
# ======================================================================

# ---- Level 1 ----
p1 = 49383540788757109209399937015403058078091585436614706959465496296978436108887
a1 = 55685723875233231914244109412725461970324405506250247848835714736428531894083
b1 = 14465416621366336584787787222004413359301857947979225099379614554383512880491
k  = 17863723127130927912437094121795715840619733807126707833630214910470361917913
c1 = (41878742451091353952894887712068645971005265624587580702506356899238014833578,
      33882347397378893053663991901529711743049843524447349970546724946010958254490)
c2 = (32044441001201280220364823846903588184438951716534669244501751822900705328405,
      20808501842510819101565506724685661870434821018672081897206182291278825489793)
cipher = 8126088154459418019024039065681028044223135048676741656267021276727337263061

# ---- Level 2 ----
p2 = 12506217790875063466368723611056175369923
A2 = 12506217790875063466368723611052784275139
B2 = 12506217790875063466368723533070038257347
P = (12209581121985501571384146459209070740325, 343933414533064030464400914099323495391)
Q = (6578542526388549877571325989098572012221, 1792660825364939960209890135582772010119)


# ======================================================================
# 有限域 GF(p) 上的椭圆曲线运算 (短 Weierstrass: y^2 = x^3 + a4*x + a6)
# ======================================================================
def inv(a, p):
    return pow(a % p, -1, p)

def ec_add(P, Q, a4, p):
    if P is None: return Q
    if Q is None: return P
    x1, y1 = P
    x2, y2 = Q
    if x1 == x2 and (y1 + y2) % p == 0:
        return None  # 无穷远点 O
    if x1 == x2 and y1 == y2:
        m = (3 * x1 * x1 + a4) * inv(2 * y1, p) % p
    else:
        m = (y2 - y1) * inv((x2 - x1) % p, p) % p
    x3 = (m * m - x1 - x2) % p
    y3 = (m * (x1 - x3) - y1) % p
    return (x3, y3)

def ec_mul(scalar, P, a4, p):
    R = None
    base = P
    while scalar > 0:
        if scalar & 1:
            R = ec_add(R, base, a4, p)
        base = ec_add(base, base, a4, p)
        scalar >>= 1
    return R

def ec_neg(P, p):
    return None if P is None else (P[0], (-P[1]) % p)

def n2s(n):
    return b"" if n == 0 else n.to_bytes((n.bit_length() + 7) // 8, "big")


# ======================================================================
# Smart's attack: 异常曲线上求解 ECDLP  Q = m2 * P
# 实现: 纯 Python p-adic (Qp) 算术 + 形式群参数 phi = -x/y
# ======================================================================
class Padic:
    """p-adic 数, 表示为 (valuation v, mantissa m), m 存为 mod p^M 的单位部分"""
    __slots__ = ("v", "m", "p", "M", "PM")

    def __init__(self, v, m, p, M, PM):
        self.p = p
        self.M = M
        self.PM = PM
        self.v = v
        self.m = m % PM
        self._norm()

    def _norm(self):
        if self.m == 0:
            self.v = self.M + 20
            return
        while self.m % self.p == 0:
            self.m //= self.p
            self.v += 1
        self.m %= self.PM


def psmart_solve(P, Q, p, a4, b, M=20):
    PM = p ** M

    def pneg(a):  return Padic(a.v, (-a.m) % PM, p, M, PM)
    def pmul(a, b): return Padic(a.v + b.v, (a.m * b.m) % PM, p, M, PM)
    def pinv(a):   return Padic(-a.v, pow(a.m, -1, PM), p, M, PM)
    def pdiv(a, b): return pmul(a, pinv(b))

    def padd(a, b):
        # 关键: 对齐阶时, 缩放 VALUATION 更大的项降下来
        # unit = u_small + u_big * p^(v_big - v_small)
        if a.v > b.v:
            a, b = b, a
        e = b.v - a.v
        t = (b.m * (p ** e)) % PM if e < M else 0
        return Padic(a.v, (a.m + t) % PM, p, M, PM)

    def psub(a, b): return padd(a, pneg(b))

    def lift_point(pt, sign):
        x = Padic(0, pt[0], p, M, PM)
        y2 = pmul(pmul(x, x), x)
        y2 = padd(y2, pmul(Padic(0, a4, p, M, PM), x))
        y2 = padd(y2, Padic(0, b, p, M, PM))
        # y = sqrt(y2), 初值取 pt[1] (其模 p 即为根), Hensel 提升到 mod p^M
        r = (pt[1] if sign > 0 else (-pt[1]) % p)
        for _ in range(120):
            r = (r - (r * r - y2.m) * pow(2 * r, -1, PM)) % PM
            if (r * r - y2.m) % PM == 0:
                break
        return (x, Padic(0, r, p, M, PM))

    def pec_add(Pt, Qt):
        if Pt is None: return Qt
        if Qt is None: return Pt
        x1, y1 = Pt
        x2, y2 = Qt
        if x1.v == x2.v and x1.m == x2.m:
            if pneg(y1).v == y2.v and pneg(y1).m == y2.m:
                return None
            num = Padic(0, (3 * x1.m * x1.m + a4) % PM, p, M, PM)
            sl = pdiv(num, Padic(0, (2 * y1.m) % PM, p, M, PM))
        else:
            sl = pdiv(psub(y2, y1), psub(x2, x1))
        x3 = psub(psub(pmul(sl, sl), x1), x2)
        y3 = psub(pmul(sl, psub(x1, x3)), y1)
        return (x3, y3)

    def pec_mul(scalar, Pt):
        R = None
        base = Pt
        while scalar > 0:
            if scalar & 1:
                R = pec_add(R, base)
            base = pec_add(base, base)
            scalar >>= 1
        return R

    def phi(pt):
        x, y = pt
        return pdiv(pneg(x), y)   # -x / y

    verified = set()
    for sP in (1, -1):
        for sQ in (1, -1):
            pP = pec_mul(p, lift_point(P, sP))
            pQ = pec_mul(p, lift_point(Q, sQ))
            if pP is None or pQ is None:
                continue
            kp = pdiv(phi(pQ), phi(pP))
            if kp.v != 0:
                continue
            cand = kp.m % p
            if ec_mul(cand, P, a4, p) == Q:   # 在 GF(p) 上校验
                verified.add(cand)
    return verified


# ======================================================================
# 解题主流程
# ======================================================================
def solve_level1():
    # m = c1 - k*c2   (k 已知)
    m = ec_add(c1, ec_neg(ec_mul(k, c2, a1, p1), p1), a1, p1)
    # cipher = m1 * m.x  (模 p1 意义下)
    m1 = (cipher * inv(m[0], p1)) % p1
    return n2s(m1)


def solve_level2():
    # 异常性检查: p2 * P 应为无穷远点
    assert ec_mul(p2, P, A2, p2) is None, "曲线不是异常曲线 (p*P != O)"
    cands = psmart_solve(P, Q, p2, A2, B2)
    assert cands, "Smart's attack 未恢复离散对数"
    cand = next(iter(cands))
    return n2s(cand)


if __name__ == "__main__":
    half1 = solve_level1()
    half2 = solve_level2()
    flag = half1 + half2
    print("Level1 前半段 :", half1)
    print("Level2 后半段 :", half2)
    print("FLAG          :", flag.decode("ascii", "replace"))

'''
ecc-no 解题报告
Flag
flag{1eo0kuvanq6vghtlpswe}
题目结构 (task.sage)
m1 = s2n(flag[:len(flag)//2])   # flag 前半段
m2 = s2n(flag[len(flag)//2:])   # flag 后半段

def lev1(m1):
    p = random_prime(2^256); a,b = random_prime(2^256), random_prime(2^256)
    E = EllipticCurve(GF(p),[a,b])
    m = E.random_point(); G = E.random_point()
    k = random_prime(2^256)          # <-- k 直接打印出来！
    K = k*G; r = random_prime(2^256)
    c1 = m + r*K; c2 = r*G
    cipher = m1 * m[0]               # m[0] = m 的 x 坐标
    # 输出 p,a,b,k,E,c1,c2,cipher

def lev2(m2):
    p = 12506217790875063466368723611056175369923
    A,B = ...; E = EllipticCurve(GF(p),[A,B])
    P = E.random_point(); Q = m2*P
    # 输出 E,P,Q
Level 1 —— k 直接泄露（送分）
c1 = m + r*K，而 K = k*G，c2 = r*G，所以 r*K = r*(k*G) = k*(r*G) = k*c2
于是 m = c1 - k*c2（已知 k，直接在曲线上做椭圆曲线减法）
cipher = m1 * m.x，注意关系是 模 p₁ 的：m1 ≡ cipher * m.x^(-1) (mod p₁)
解得前半段：flag{1eo0kuva
Level 2 —— ECDLP on anomalous curve（Smart 攻击）
p₂ ≈ 134 bit，p₂·P = O（验证通过）→ #E(Fp₂) = p₂，即 trace=1 的异常曲线（anomalous）
素数阶曲线无法用 Pohlig–Hellman，只能用 Smart's attack（p-adic / 形式群）
算法：把 P,Q 提升到 E(Qp)，计算 p·P̃、p·Q̃，取形式参数 phi = -x/y，
则离散对数 m2 ≡ phi(p·Q̃) / phi(p·P̃) (mod p₂)
解得 m2 = 8750135523819934696348860245373 → 后半段 nq6vghtlpswe}
验证：m2 · P == Q（在 Fp₂ 上）成立
实现要点（纯 Python，无 sage）
自写 p-adic 类 (valuation v, mantissa m)，m 存为 mod p^M
致命坑：padd 对齐阶时，必须缩放高阶（valuation 更大）的 term 降下来：
unit = u_small + u_big * p^(v_big - v_small)；
拆错项会让单位部分完全算错、离散对数失真。
提升点：x = P.x，y = sqrt(x³+Ax+B) 用 Hensel 提升（初值取 P.y 即其模 p 根）
M=20 精度足够（实际只需 ≥2）
验证
Level1: m1 = cipher * inv(m.x, p1) % p1 → b'flag{1eo0kuva'
Level2: 8750135523819934696348860245373 · P == Q (mod p₂) → True
拼接：flag{1eo0kuva + nq6vghtlpswe} = flag{1eo0kuvanq6vghtlpswe}
'''