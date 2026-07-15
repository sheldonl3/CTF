import angr
import claripy

def main():
    # 加载二进制文件（请确保路径正确）
    proj = angr.Project("./code", auto_load_libs=False)

    # ---------- 1. 符号化三个命令行参数 ----------
    arg1 = claripy.BVS("arg1", 8 * 32)
    arg2 = claripy.BVS("arg2", 8 * 32)
    arg3 = claripy.BVS("arg3", 8 * 32)

    # ---------- 2. 创建初始状态（必须传入符号化参数） ----------
    state = proj.factory.entry_state(args=["./code", arg1, arg2, arg3])

    # ---------- 3. 在 state 上添加约束（可打印 ASCII 字符） ----------
    # 修正1：将约束添加到 state.solver 中，而不是每次新建状态
    for bv in [arg1, arg2, arg3]:
        for i in range(32):
            byte = bv.get_byte(i)
            # 修正2：使用 claripy.Or 和 claripy.And
            state.solver.add(claripy.Or(
                byte == 0,
                claripy.And(byte >= 0x20, byte <= 0x7e)
            ))

    # ---------- 4. 获取 PIE 基址并设置目标地址 ----------
    #base = proj.loader.main_object.address
    base = proj.loader.main_object.mapped_base
    find_addr = base + 0x1391          # 打印 "Get your key: " 的指令偏移
    avoid_addrs = [
        base + 0x120D,                 # printf("what?")
        base + 0x124A,                 # printf("you are wrong, sorry.")
        base + 0x12CA,                 # printf("ha, you won't get it!")
        base + 0x1304                  # printf("so close, dude!")
    ]

    # ---------- 5. 执行探索 ----------
    sim = proj.factory.simulation_manager(state)
    sim.explore(find=find_addr, avoid=avoid_addrs)

    # ---------- 6. 提取结果 ----------
    if sim.found:
        found_state = sim.found[0]
        val1 = found_state.solver.eval(arg1, cast_to=bytes).rstrip(b'\x00')
        val2 = found_state.solver.eval(arg2, cast_to=bytes).rstrip(b'\x00')
        val3 = found_state.solver.eval(arg3, cast_to=bytes).rstrip(b'\x00')

        print("\n找到的参数为：")
        print(f"argv[1] = {val1}")   # 应为 b'51966'
        print(f"argv[2] = {val2}")   # 例：b'25'
        print(f"argv[3] = {val3}")   # 应为 b'h4cky0u'

        # 可选：手动计算 hash 验证
        hash_val = int(val1) * 31337 + (int(val2) % 17) * 11 + len(val3) - 1615810207
        print(f"计算出的 hash: {hash_val:x}")
    else:
        print("未找到可行路径，请检查地址偏移是否正确。")

if __name__ == "__main__":
    main()
