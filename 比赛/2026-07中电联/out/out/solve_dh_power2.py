#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DH over Z_{2^n}^* 离散对数攻击 (p = 2^542 是合数 -> 致命弱点)
方法: 2-adic (p-adic) 离散对数.
  Z_{2^n}^* ≅ <-1> x <5> (n>=3).
  对 v ≡ 1 (mod 4): 用 5 为基做逐位提升求 f = dlog_5(v) (mod 2^{n-2}).
  对一般 h: 写成 h = (-1)^e * 5^f, 与 g 对比得到关于 x 的同余, CRT 合并.
依赖: pycryptodome, sympy
"""
import re, hashlib, random
from Crypto.Cipher import AES

OUT = r"D:/Study/培训-检查/20260610--中电联培训/考题/红队/out/out/out"
g = 916143391925527262831875920931
p = 14396524142538228424993723224595141948383030778566133225922417832357880258148761185020930195532450742879746914027266864394266451377581759004827248578768524336431104
N = p.bit_length() - 1   # p = 2^N, N = 542
assert p == (1 << N), f"p != 2^{N}"
MOD = p

def dlog5(v, n):
    """求 f 使 5^f ≡ v (mod 2^n), 要求 v ≡ 1 (mod 4). 返回 f (mod 2^{n-2}).

    逐位 Hensel 提升:
      invariant: 5^f ≡ v (mod 2^j).
      j 从 2 起, 考察第 (j-2) 位. 候选 f' = f + 2^{j-2}.
      因 5^{2^{j-2}} ≡ 1 + 2^j (mod 2^{j+1}), 有
        5^{f'} = 5^f * 5^{2^{j-2}} ≡ v*(1+2^j) (mod 2^{j+1}).
      当且仅当 5^f ≡ v+2^j (mod 2^{j+1}) 时 (=v 不成立), 加 2^{j-2} 才能修正,
      此时 5^{f'} ≡ v (mod 2^{j+1}). 故判定条件为 '等于' 才置位.
    """
    assert v % 4 == 1, "v must be 1 mod 4"
    f = 0
    for j in range(2, n):
        if pow(5, f + (1 << (j - 2)), 1 << n) % (1 << (j + 1)) == v % (1 << (j + 1)):
            f += (1 << (j - 2))
    return f

def inv_odd(a, mod):
    """a 为奇数, 求 a 在模 2^? 下的逆 (mod 为 2 的幂)."""
    return pow(a, -1, mod)

def dlog_base_g(h, g, n):
    """求所有 x (mod 2^{n-1}) 使 g^x ≡ h (mod 2^n). g,h 为奇数. 返回候选列表."""
    e_g = 0 if g % 4 == 1 else 1
    e_h = 0 if h % 4 == 1 else 1
    v_g = g if e_g == 0 else (-g) % (1 << n)
    v_h = h if e_h == 0 else (-h) % (1 << n)
    f_g = dlog5(v_g, n)
    f_h = dlog5(v_h, n)
    M = 1 << (n - 2)
    t = (f_g & -f_g).bit_length() - 1   # f_g = 2^t * u, u odd
    assert f_h % (1 << t) == 0, "f_h 不满足可解条件"
    fg2 = f_g >> t
    fh2 = f_h >> t
    M2 = M >> t
    x0 = (fh2 * inv_odd(fg2, M2)) % M2   # x ≡ x0 (mod M2)
    cands = []
    for kk in range(1 << t):
        x = x0 + kk * M2
        if e_g == 0:
            cands.append(x)
        else:
            if (x % 2) == (e_h % 2):
                cands.append(x)
    # 校验, 仅保留真正满足 g^x == h 的 (多值来自 2-adic 提升)
    out = [x for x in cands if pow(g, x, 1 << n) == h % (1 << n)]
    return out

def parse():
    data = open(OUT, 'rb').read().decode('utf-8', 'replace')
    A = B = C1 = C2 = None
    for line in [x for x in data.split('\n') if x.strip()]:
        hdr, body = line.split(':', 1)
        b = [int(t, 16) for t in body.split()]
        typ = b[6]; pb = bytes(b[7:])
        if typ == 1 and len(b[7:]) >= 16:
            s = re.sub(r'[^0-9a-fA-F]', '', pb.decode('ascii'))
            if '主站->子站' in hdr and A is None:
                A = int(s, 16)
            elif '子站->主站' in hdr and B is None:
                B = int(s, 16)
        elif typ == 2:
            if '主站->子站' in hdr and C1 is None:
                C1 = pb
            elif '子站->主站' in hdr and C2 is None:
                C2 = pb
    return A, B, C1, C2

def decrypt_try(key, ct):
    pt = AES.new(key, AES.MODE_ECB).decrypt(ct)
    return pt, pt.rstrip(b'\x00')

def self_test():
    print("[*] 自检测试 dlog_base_g ...")
    random.seed(12345)
    for trial in range(8):
        a = random.getrandbits(300)
        A = pow(g, a, MOD)
        cands = dlog_base_g(A, g, N)
        assert any(pow(g, x, MOD) == A for x in cands), f"DLP 求解失败 trial{trial}"
    for a in [1,2,3,4,5,100,1000,12345]:
        A = pow(g, a, MOD)
        cands = dlog_base_g(A, g, N)
        assert any(pow(g, x, MOD) == A for x in cands), f"small a={a} failed"
    print("[*] 自检测试通过 (全部返回正确 coset 候选)")

def main():
    self_test()
    A, B, C1, C2 = parse()
    print("A bits:", A.bit_length(), "B bits:", B.bit_length())
    print("C1(主站->子站) len:", None if C1 is None else len(C1),
          "C2(子站->主站) len:", None if C2 is None else len(C2))
    assert A and B, "未解析到 DH 公钥 A/B"
    cands_a = dlog_base_g(A, g, N)
    cands_b = dlog_base_g(B, g, N)
    print(f"[*] a 候选数 {len(cands_a)}, b 候选数 {len(cands_b)}")

    found = False
    for a in cands_a:
        for b in cands_b:
            sA = pow(B, a, MOD)   # 子站视角: shared = B^a
            sB = pow(A, b, MOD)   # 主站视角: shared = A^b
            if sA != sB:
                continue
            shared = sA
            key = hashlib.sha256(str(shared).encode()).hexdigest()[:16].encode()
            ok = True
            texts = {}
            for name, ct in [("C1 主站->子站", C1), ("C2 子站->主站", C2)]:
                if ct is None:
                    continue
                pt, ptu = decrypt_try(key, ct)
                texts[name] = (pt, ptu)
            # 至少一个明文看起来像 flag / 可打印
            looks = any(
                (ptu.startswith(b'flag') or b'flag' in ptu or ptu.isprintable())
                for (_, ptu) in texts.values()
            )
            if looks:
                print(f"\n[+] 命中共享密钥! a(mod coset)=... b(mod coset)=...")
                print("sharekey =", key.decode())
                for name, (pt, ptu) in texts.items():
                    print(f"[{name}] 明文: {pt!r}")
                    print(f"          去填充: {ptu!r}")
                found = True
                break
        if found:
            break
    if not found:
        # 退化: 尝试所有组合并直接打印, 由人工查看
        print("[!] 自动识别 flag 失败, 输出全部候选明文:")
        for a in cands_a[:4]:
            for b in cands_b[:4]:
                sA, sB = pow(B, a, MOD), pow(A, b, MOD)
                shared = sA if sA == sB else sA
                key = hashlib.sha256(str(shared).encode()).hexdigest()[:16].encode()
                for name, ct in [("C1", C1), ("C2", C2)]:
                    if ct is None: continue
                    pt, ptu = decrypt_try(key, ct)
                    print(f"a={a} b={b} {name}: {ptu!r}")

if __name__ == '__main__':
    main()
