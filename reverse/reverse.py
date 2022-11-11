#!/usr/bin/env python
# -*- coding:utf-8 -*-

infile = file("flag.png", "rb")
#outfile = file("out.txt", "wb")


def main():
    hex_list = []
    while 1:
        c = infile.read(1)
        if not c:
            break
        hex_list.append(hex(ord(c))[2:])
    hex_list.reverse()
    infile.close()
    # outfile.writelines(hex_list)
    # outfile.close()
    ccfile = file("cc.png", "wb")
    for x in hex_list:
        if len(x) == 1:
            x = '0' + x
        print x
        ccfile.write(x.decode("hex"))

if __name__ == '__main__':
    main()



