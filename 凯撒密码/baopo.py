#!/usr/bin/env python
# -*- coding:utf-8 -*-

import hashlib

dic=['q','w','e','r','t','y','u','i','o','a','s','d','f','g','h','j','k','p','l','z','x','c','v','b','n','m','0','1','2','3','4','5','6','7','8','9']
for a in range(len(dic)):
    for b in range(len(dic)):
        for c in range(len(dic)):
                m=dic[a]+dic[b]+dic[c]
                flag=hashlib.md5()
                flag.update(m.encode("utf-8"))
                md5=flag.hexdigest()
                if md5=='29c1dd3af5bb698efd81ca5bc1178e5f':
                            print (m)
