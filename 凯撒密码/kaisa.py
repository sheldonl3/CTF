#!/usr/bin/env python
# -*- coding:utf-8 -*-

def convertChar(ciphertext, offset):
    chars = "abcdefghijklmnopqrstuvwxyz"
    for char in ciphertext:
        is_upper_flag = 0
        if char.isupper():
            char = char.lower()
            is_upper_flag = 1

        if char not in chars:
            outputChar(is_upper_flag, char)
            continue

        tempchar_ascii = ord(char) + offset
        tempchar = chr(tempchar_ascii)
        if tempchar not in chars:
            if offset < 0:
                tempchar_ascii += len(chars)
            else:
                tempchar_ascii -= len(chars)
        tempchar = chr(tempchar_ascii)
        outputChar(is_upper_flag, tempchar)
    print("")


def outputChar(is_upper_flag, char):
    if is_upper_flag == 1:
        print(char.upper(), end="")
    else:
        print(char, end="")

a = [109, 115, 104, 110, 123, 108, 53, 55, 105, 57, 108, 49, 56, 105, 48, 56, 105, 109, 109, 48, 107, 48, 53, 104, 51, 106, 53, 57, 57, 48, 48, 105, 49, 48, 63, 63, 63, 125, 116, 107, 53, 58, 50, 57, 106, 49, 107, 107, 51, 104, 109, 53, 105, 105, 54, 57, 56, 108, 109, 107, 56, 49, 106, 104, 53, 105, 106, 49, 49, 55, 56, 108, 53, 109]
flag = ''
for i in range(len(a)):
    flag+=chr(a[i])
print(flag)
for i in range(27):
    convertChar(flag, i)
