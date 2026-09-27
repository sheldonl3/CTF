#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ook! 离线解码器 (纯标准库, 无第三方依赖, 无交互)

用法:
    1) 把 Ook! 文本粘贴到下面的 OOK_TEXT 里
    2) python ook_decode.py
"""

# ==================== 把 Ook! 文本粘贴到这里 ====================
OOK_TEXT = """
Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook!
Ook? Ook! Ook! Ook. Ook? Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook.
Ook. Ook. Ook. Ook. Ook? Ook. Ook? Ook! Ook. Ook? Ook! Ook. Ook. Ook. Ook!
Ook. Ook. Ook. Ook! Ook. Ook? Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook! Ook?
Ook! Ook! Ook. Ook? Ook. Ook. Ook. Ook. Ook. Ook. Ook? Ook. Ook? Ook! Ook.
Ook? Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook! Ook. Ook? Ook.
Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook! Ook? Ook! Ook! Ook. Ook? Ook.
Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook? Ook. Ook? Ook! Ook. Ook? Ook. Ook.
Ook. Ook. Ook! Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook!
Ook. Ook? Ook. 
"""
# ================================================================

# ---------- 可选开关 ----------
AUTO_SWAP = True    # 自动纠正"打印/读取被打反"的样本 (0 个 . 却有 , 时自动互换)
FORCE_SWAP = False  # 强制互换打印/读取指令, 不管自动检测结论
PRINT_BF = True     # 是否打印等价的 Brainfuck 代码

# Ook! 词对 -> Brainfuck 指令
OOK_PAIRS = {
    ("Ook.", "Ook?"): ">",
    ("Ook?", "Ook."): "<",
    ("Ook.", "Ook."): "+",
    ("Ook!", "Ook!"): "-",
    ("Ook.", "Ook!"): ".",
    ("Ook!", "Ook."): ",",
    ("Ook!", "Ook?"): "[",
    ("Ook?", "Ook!"): "]",
}


def normalize_token(tok):
    """归一化到标准 Ook 词, 兼容小写 ook。"""
    low = tok.strip().lower()
    if low == "ook.":
        return "Ook."
    if low == "ook?":
        return "Ook?"
    if low == "ook!":
        return "Ook!"
    return None


def ook_to_bf(text):
    """把 Ook! 文本转成 Brainfuck 代码串 (会忽略文本里的非 Ook 字符)。"""
    import re
    tokens = re.findall(r"Ook[.!?]", text, flags=re.IGNORECASE)
    norm = [normalize_token(t) for t in tokens]
    norm = [t for t in norm if t]

    if len(norm) % 2 != 0:
        raise ValueError(
            "Ook! token 数量为奇数 ({}), 无法两两配对, 请检查文本是否完整".format(len(norm))
        )

    bf = []
    for i in range(0, len(norm), 2):
        pair = (norm[i], norm[i + 1])
        if pair not in OOK_PAIRS:
            raise ValueError("无法识别的词对: {} {} (位置 {})".format(*pair, i))
        bf.append(OOK_PAIRS[pair])
    return "".join(bf)


def swap_io_code(bf):
    """把 Brainfuck 里的 <打印 .> 与 <读取 ,> 指令互换。

    对应 Ook! 层两对被打反:   Ook. Ook! (.)  <->  Ook! Ook. (,)
    """
    return bf.replace(",", "\x00").replace(".", ",").replace("\x00", ".")


def should_auto_swap(bf):
    """判定是否被打反: 0 个打印指令却有读取指令。"""
    return bf.count(".") == 0 and bf.count(",") > 0


def run_brainfuck(code, inp=b"", cells=30000, max_steps=5_000_000):
    """极简 Brainfuck 解释器, 返回程序的输出字节。"""
    tape = [0] * cells
    ptr = 0
    ip = 0
    out = bytearray()
    inp_buf = bytearray(inp)
    inp_pos = 0
    steps = 0

    # 预计算 [ ] 匹配
    bracket = {}
    stack = []
    for i, c in enumerate(code):
        if c == "[":
            stack.append(i)
        elif c == "]":
            if not stack:
                raise ValueError("多余的 ] 在位置 {}".format(i))
            j = stack.pop()
            bracket[j] = i
            bracket[i] = j
    if stack:
        raise ValueError("未闭合的 [ 在位置 {}".format(stack[-1]))

    while ip < len(code):
        steps += 1
        if steps > max_steps:
            raise RuntimeError("步数超过上限 {}, 疑似死循环".format(max_steps))
        c = code[ip]
        if c == ">":
            ptr = (ptr + 1) % cells
        elif c == "<":
            ptr = (ptr - 1) % cells
        elif c == "+":
            tape[ptr] = (tape[ptr] + 1) % 256
        elif c == "-":
            tape[ptr] = (tape[ptr] - 1) % 256
        elif c == ".":
            out.append(tape[ptr] & 0xFF)
        elif c == ",":
            if inp_pos < len(inp_buf):
                tape[ptr] = inp_buf[inp_pos]
                inp_pos += 1
            else:
                tape[ptr] = 0
        elif c == "[":
            if tape[ptr] == 0:
                ip = bracket[ip]
        elif c == "]":
            if tape[ptr] != 0:
                ip = bracket[ip]
        ip += 1
    return bytes(out)


def main():
    bf = ook_to_bf(OOK_TEXT)

    # 互换打印/读取指令
    if FORCE_SWAP or (AUTO_SWAP and should_auto_swap(bf)):
        bf = swap_io_code(bf)
        print("=== [自动纠正] 该样本打印/读取指令被打反, 已互换 Ook. Ook! <-> Ook! Ook. ===")

    if PRINT_BF:
        print("=== Brainfuck (等价代码) ===")
        print(bf)

    out = run_brainfuck(bf)

    print("=== 输出 ===")
    try:
        print(out.decode("utf-8", errors="replace"))
    except Exception:
        pass
    # 同时给出原始字节 (flag 常含非打印字符)
    print("=== 输出(hex) ===")
    print(out.hex())
    return out


if __name__ == "__main__":
    main()
