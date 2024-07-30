# encoding: utf-8
import sys

def brainfuck_decode(code):
    # 初始化内存和指针
    memory = [0] * 30000
    pointer = 0

    # 结果字符串
    result = ""

    # 循环遍历 Brainfuck 代码
    i = 0
    while i < len(code):
        char = code[i]

        if char == '>':
            pointer += 1
        elif char == '<':
            pointer -= 1
        elif char == '+':
            memory[pointer] += 1
        elif char == '-':
            memory[pointer] -= 1
        elif char == '.':
            result += chr(memory[pointer])
        elif char == ',':
            # 这里需要实现读取用户输入的逻辑
            pass
        elif char == '[':
            # 如果当前指针所在的内存位置为0，则跳转到与之对应的"]"之后
            if memory[pointer] == 0:
                loop_count = 1
                while loop_count > 0:
                    i += 1
                    if code[i] == '[':
                        loop_count += 1
                    elif code[i] == ']':
                        loop_count -= 1
            else:
                # 否则继续执行下面的指令
                pass
        elif char == ']':
            # 如果当前指针所在的内存位置不为0，则跳转到与之对应的"["之前
            if memory[pointer] != 0:
                loop_count = 1
                while loop_count > 0:
                    i -= 1
                    if code[i] == ']':
                        loop_count += 1
                    elif code[i] == '[':
                        loop_count -= 1
                # 因为循环结束后还会+1，所以这里需要减去1
                i -= 1
            else:
                # 否则继续执行下面的指令
                pass

        i += 1

    return result

brainfuck_code = '''+++++ +++++ [->++ +++++ +++<] >++.+ +++++ .<+++ [->-- -<]>- -.+++ +++.<
++++[ ->+++ +<]>+ +++.< +++++ +[->- ----- <]>-- ----- --.<+ +++[- >----
<]>-- ----- .<+++ [->++ +<]>+ +++++ .<+++ +[->- ---<] >-.<+ +++++ [->++
++++< ]>+++ +++.< +++++ [->-- ---<] >---- -.+++ .<+++ [->-- -<]>- ----- .<'''
decoded_string = brainfuck_decode(brainfuck_code)
print("Brainfuck解码后：" + decoded_string)
