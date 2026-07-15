import z3
x = z3.Int(name = 'x')

s = z3.Solver()

s.add(11*x*x+17*x*x*x*x-13*x*x*x-7*x == 198)
print(s.check())

if s.check() == z3.sat:     # .sat有解 .unsat无解 .unknown未知
    print(s.model())        # 打印
