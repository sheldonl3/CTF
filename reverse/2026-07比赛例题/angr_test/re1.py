import angr
import claripy

def main():
    # 加载二进制（自动处理 PIE）
    proj = angr.Project("./code", auto_load_libs=False)

    # 符号化三个参数（每个 16 字节，足够表示预期值）
    arg1 = claripy.BVS("arg1", 8 * 16)
    arg2 = claripy.BVS("arg2", 8 * 16)
    arg3 = claripy.BVS("arg3", 8 * 16)

    # 创建初始状态（所有参数均为符号变量）
    state = proj.factory.entry_state(args=["./code", arg1, arg2, arg3])

    '''
          交互方式则
    stdin_content = claripy.Concat(input1, claripy.BVV(b'\n'), input2, claripy.BVV(b'\n'), input3, claripy.BVV(b'\n'))
    '''


    # ---------- 添加约束，规范输入格式 ----------
    # arg1 和 arg2 必须是纯数字串，以 \x00 结尾
    for bv in [arg1, arg2]:
        for i in range(15):
            byte = bv.get_byte(i)
            state.solver.add(claripy.Or(
                byte == 0,
                claripy.And(byte >= ord('0'), byte <= ord('9'))
            ))
        #state.solver.add(bv.get_byte(15) == 0)

    # arg3 必须是可打印 ASCII 且以 \x00 结尾（具体内容由路径条件推导）
    for i in range(15):
        byte = arg3.get_byte(i)
        state.solver.add(claripy.Or(
            byte == 0,
            claripy.And(byte >= 0x20, byte <= 0x7e)
        ))
    state.solver.add(arg3.get_byte(15) == 0)

    # 限制 arg2 的位数不超过 5 位（即 ≤ 99999），确保有限数量的解
    state.solver.add(arg2.get_byte(5) == 0)

    # ---------- 获取 PIE 基址 ----------
    base = proj.loader.main_object.mapped_base
    find_addr = base + 0x1391
    avoid_addrs = [
        base + 0x120D,
        base + 0x124A,
        base + 0x12CA,
        base + 0x1304
    ]
    solution_count = 0
    max_solutions = 1  # 修改为 5
    # ---------- 循环求解，最多找 5 组 ----------
    print("正在使用 angr 自动求解所有三个参数...")
    print(f"每找到一组解会立即打印\n，最多打印{max_solutions}组")


    while solution_count < max_solutions:
        sim = proj.factory.simulation_manager(state)
        sim.explore(find=find_addr, avoid=avoid_addrs)

        if not sim.found:
            break  # 无更多解

        found_state = sim.found[0]

        # 提取三个参数的字节串
        val1_bytes = found_state.solver.eval(arg1, cast_to=bytes).split(b'\x00', 1)[0]
        val2_bytes = found_state.solver.eval(arg2, cast_to=bytes).split(b'\x00', 1)[0]
        val3_bytes = found_state.solver.eval(arg3, cast_to=bytes).split(b'\x00', 1)[0]
        print("arg1-->",arg1)
        print("val1_bytes-->",val1_bytes)
        print("arg2-->",arg1)
        print("val2_bytes-->",val2_bytes)
        # 转换为 Python 类型

        val1 = int(val1_bytes)
        val2 = int(val2_bytes)
        val3 = val3_bytes.decode('ascii')


        solution_count += 1
        # 立即打印找到的这组解
        print(f"解 #{solution_count}:")
        print(f"  argv[1] = {val1} (bytes: {val1_bytes})")
        print(f"  argv[2] = {val2} (bytes: {val2_bytes})")
        print(f"  argv[3] = {val3} (bytes: {val3_bytes})")
        # 计算并输出 hash
        hash_val = val1 * 31337 + (val2 % 17) * 11 + len(val3) - 1615810207
        print(f"  对应 hash: {hash_val:x}\n")

        # 排除当前找到的整组解（三个变量均相同）
        state.solver.add(claripy.Not(claripy.And(
            arg1 == found_state.solver.eval(arg1, cast_to=bytes),
            arg2 == found_state.solver.eval(arg2, cast_to=bytes),
            arg3 == found_state.solver.eval(arg3, cast_to=bytes)
        )))

    if solution_count == 0:
        print("未找到任何解。")
    else:
        print(f"共找到 {solution_count} 组解（已达到设定的最大打印数 {max_solutions}）。")
        #print("注意：arg1 和 arg3 由 angr 自动推导得出，arg2 由于条件限制有无限多个，此处仅展示有限范围内的前 5 组。")

if __name__ == "__main__":
    main()
