ciphertext = "H@^jHwpsH)[jH{M/\\tBBK_|-O{W.iJZ7\\)|~zaB^H+Lwv{SS|-j@\\_[Y"
res=""
for i in ciphertext:
        res+=(chr(ord(i) ^ 0x18))
    
print(res)