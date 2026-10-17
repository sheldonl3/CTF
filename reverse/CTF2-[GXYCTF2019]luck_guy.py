# luck_guy (SWAT2019 CTF, "Designed by Solar") — 静态重建 flag
#
# 程序逻辑 (capstone 反汇编 + .rodata/.data 字符串核对):
#   main: 读 "lucky number" -> patch_me(奇偶) -> 总是调 get_flag
#   get_flag:
#     srand(time(0)); 循环 5 次, 每次 v = rand() % 200, switch(v):
#       case 1: printf("OK, it's flag: %s", first_part + buf2)   # 打印
#       case 4: strcat(buf2, "icug`of\x7f")                      # 构造后半
#       case 5: for j in 0..7: buf2[j] -= (1 if j偶 else 2)        # 变换后半
#       default: puts("emmm,you can't find flag 23333")
#   随机序列几乎不可能自然命中 3->4->0, 故提示 "try to patch me and find flag"
#
# 静态重建: 第一半在 .data(0x601078), 后半由 case3+case4 推导, 与随机种子无关。

first_part='GXY{do_not_'

# case3 构造的局部串 (get_flag 0x4008d6..0x4008f2 的立即数字节)
buf2 = bytes([0x69, 0x63, 0x75, 0x67, 0x60, 0x6f, 0x66, 0x7f])   # "icug`of\x7f"
print("buf2 after case3 (strcat):", repr(buf2.decode('latin1')))

# case4 变换: 偶数位 -1, 奇数位 -2
out = bytearray(buf2)
for j in range(8):
    out[j] = (out[j] - (1 if j % 2 == 0 else 2)) & 0xff
buf2_trans = out.decode('latin1')
print("buf2 after case4 (transform):", repr(buf2_trans))

flag = first_part + buf2_trans
print(flag)