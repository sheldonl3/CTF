from binascii import *
from base64 import *

'''
攻防世界 GFSJ0839 crypto 工业信息安全技能大赛个人线上赛 简单流量分析
将这些ICMP请求包中的data字段数据提取出来，返回包的数据和请求包是一样的，拼接成完整包
先用tshark: tshark -r fetus_pcap.pcap -Y 'ip.src_host=="192.168.3.73"' -e data -T fields > icmp_data.txt
在用脚本处理icmp_data.txt
'''
base64_data = ''
with open('icmp_data.txt', 'r') as f:
    lines = f.readlines()
    for line in lines:
        line = unhexlify(line.strip())
        asc_code = int(len(line))
        base64_data += chr(asc_code)
print(b64decode(base64_data))