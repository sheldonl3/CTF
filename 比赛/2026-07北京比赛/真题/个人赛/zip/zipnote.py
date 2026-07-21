import zipfile

z = zipfile.ZipFile("white-no.zip")
c = z.comment.decode('latin1')
print(repr(c))                       # 看清到底是空格还是 \t
lines = [l for l in c.replace('\x00','').split('\r\n') if l]
# 空格=0, Tab=1, 高位在前 → 8位一行 → 16进制
out = bytes(int(''.join('1' if ch=='\t' else '0' for ch in ln)[:8], 2) for ln in lines)
print(out)                           # b'84f87c02f4ea63dd'

'''
# white-no 解题报告

## 目标
文件：`个人赛/white-no/white`（5,120,032 字节，名为 `white`）
目标：从该文件中找出隐藏的 flag。

## 分析过程
1. **文件初判**：`file` 识别为 `data`，无标准文件头。
2. **熵分析**：字节熵高达 **7.999966 bit/byte**，256 种字节值分布完全均匀；RGB 三通道相等像素数（29）与纯随机期望（26）一致；无任何可读明文 / `flag{` 字样。
   → 判定该 5MB 文件是**均匀随机数据（白噪声）**，本身不含明文 flag，是一个**诱饵（decoy）**。
3. **单字节 / 重复密钥 XOR、OpenSSL、LSB/比特平面隐写**等一系列对 `white` 文件本身的尝试均无结果，进一步确认 `white` 文件不可直接还原。
4. **关键转折**：注意到原始压缩包 `个人赛/white-no.zip` 的**注释（ZIP comment）由空格和制表符（Tab）组成**——这正是 “white（空白字符）” 双关所指的**空白字符隐写（whitespace steganography）**。

## 解码
将 ZIP 注释按 `\r\n` 切分为 16 行，每行 8 个空白字符：
- 空格 ` ` = 0
- 制表符 `\t` = 1
- 每行 8 位，高位（MSB）在前 → 1 字节

解码结果（16 字节，全部为合法十六进制字符，验证映射正确）：

```
84f87c02f4ea63dd
```

## 结论
隐藏的 flag 内容即为该十六进制串。按照本次培训统一的提交格式 `flag{...}`，最终 flag 为：

```
flag{84f87c02f4ea63dd}
```

> 说明：`white` 这个 5MB 随机文件是干扰项，真正的 flag 藏在压缩包注释的空白字符里。

'''