def encode(line, key, key2):
    return ''.join(chr(x ^ ord(line[x]) ^ ord(key[::-1][x]) ^ ord(key2[x])) for x in range(len(line)))

flag = encode('-M7\x10w\x10`h1\t e}\x0eO_cQ(D\x18\x1a_\x17!hS1\x02\x0e\x14\r!\x00-{\x17o\x10[JG', 'GQIS5EmzfZA1Ci8NslaoMxPXqrvFB7hYOkbg9y20W3', 'xwdFqMck1vA0pl7B8WO3DrGLma4sZ2Y6ouCPEHSQVT')
print(flag)