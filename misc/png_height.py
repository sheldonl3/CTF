import binascii
import struct

'''
图片高度隐藏
故意修改了图片高度导致内容显示不全，需要重新计算、修改高度
[BJDCTF2020]一叶障目
'''
crc32key = 0x370C8F0B
for i in range(0, 65535):
    height = struct.pack('>i', i)
    header = b"\x49\x48\x44\x52"
    width = b"\x00\x00\x01\xF4"
    color = b"\x08\x02\x00\x00\x00"
    data = header + width + height + color
    crc32result = binascii.crc32(data) & 0xffffffff
    if crc32result == crc32key:
        hex_height = ' '.join(f'{x:02X}' for x in height)
        print(hex_height)
        break
