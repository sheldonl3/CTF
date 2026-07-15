from z3 import *

'''
pip install z3-solver
鸡兔同笼问题
头共20
脚共56
求鸡多少只，兔多少只
'''


# 1. 定义变量：兔子和鸡的数量（整数）
rabbits = Int('rabbits')
chickens = Int('chickens')

# 2. 创建求解器并添加约束
solver = Solver()

# 约束1: 数量不能为负
solver.add(rabbits >= 0)
solver.add(chickens >= 0)
# 约束2: 头数总和
solver.add(rabbits + chickens == 20)
# 约束3: 脚数总和
solver.add(4 * rabbits + 2 * chickens == 56)

# 3. 检查是否有解并打印结果
if solver.check() == sat:
    model = solver.model()
    print(f"兔子有 {model[rabbits]} 只")
    print(f"鸡有 {model[chickens]} 只")
else:
    print("无解")
