import re  
  
# 打开文件并读取内容  
with open('./源码.txt', 'r', encoding='utf-8') as file:  
    content = file.read()  
  
# 使用正则表达式匹配flag{*}格式的文本  
matches = re.findall(r'flag\{.*?\}', content)

  
# 打开flag.txt文件并写入匹配项  
with open('./flag.txt', 'w', encoding='utf-8') as file:  
    for match in matches:  
        file.write(match + '\n')  # 每个匹配项后添加一个换行符