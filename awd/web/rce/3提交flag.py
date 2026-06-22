'''
POST /competition/api/contestants/match_plan/90118/question/awd HTTP/1.1
Host: 172.19.6.100
Connection: keep-alive
Content-Length: 55
sec-ch-ua-platform: "Windows"
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36
Accept: application/json, text/plain, */*
sec-ch-ua: "Google Chrome";v="149", "Chromium";v="149", "Not)A;Brand";v="24"
Content-Type: application/json
sec-ch-ua-mobile: ?0
Origin: https://172.19.6.100
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: cors
Sec-Fetch-Dest: empty
Referer: https://172.19.6.100/competition_web/
Accept-Encoding: gzip, deflate, br, zstd
Accept-Language: zh-CN,zh;q=0.9
Cookie: sso_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJVVUlEIjoiOTlhZjgzMTMtMzE3Yi00NzQzLTgzZWEtNjE3NDMyNWNmMzAyIiwiSUQiOjE3NCwiVXNlcm5hbWUiOiJ1c2VyMTcwIiwiTmlja05hbWUiOiJ1c2VyMTcwIiwiSXNTdXBlciI6ZmFsc2UsIkxhc3RMb2dpbkF0IjoiMjAyNi0wNi0xN1QxNzoxNzoxOS4yOTMxNTY5NjMrMDg6MDAiLCJCdWZmZXJUaW1lIjowLCJpc3MiOiJxbVBsdXMiLCJuYmYiOjE3ODE2ODY4Mzl9.zYKJ9P-dIsctzR0iZun_T0x71wITFbRVLrqJ6VqaCBI; um_auth=1; competition_session=MTc4MTY4NzQxNnxOd3dBTkVveVZGTlRSMUUwVGxCVldEWTJORlZSVUZKT1FWWlpTa3hQTjBGV1VVWkZWMFZRV1ZrM1MwVldSMFpHVGtKSlJFTmFOMUU9fGB1_swchU_FzTPg0MPpBqm-gNLenWxirIZHETe36sMI

{"answer":"flag{88b4e2a3-8171-4483-b298-21f6eae06c4d}"}



POST /competition/api/contestants/match_plan/90118/question/awd HTTP/1.1
Host: 172.19.6.100
Connection: keep-alive
Content-Length: 55
sec-ch-ua-platform: "Windows"
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36
Accept: application/json, text/plain, */*
sec-ch-ua: "Google Chrome";v="149", "Chromium";v="149", "Not)A;Brand";v="24"
Content-Type: application/json
sec-ch-ua-mobile: ?0
Origin: https://172.19.6.100
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: cors
Sec-Fetch-Dest: empty
Referer: https://172.19.6.100/competition_web/
Accept-Encoding: gzip, deflate, br, zstd
Accept-Language: zh-CN,zh;q=0.9
Cookie: sso_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJVVUlEIjoiOTlhZjgzMTMtMzE3Yi00NzQzLTgzZWEtNjE3NDMyNWNmMzAyIiwiSUQiOjE3NCwiVXNlcm5hbWUiOiJ1c2VyMTcwIiwiTmlja05hbWUiOiJ1c2VyMTcwIiwiSXNTdXBlciI6ZmFsc2UsIkxhc3RMb2dpbkF0IjoiMjAyNi0wNi0xN1QxNzoxNzoxOS4yOTMxNTY5NjMrMDg6MDAiLCJCdWZmZXJUaW1lIjowLCJpc3MiOiJxbVBsdXMiLCJuYmYiOjE3ODE2ODY4Mzl9.zYKJ9P-dIsctzR0iZun_T0x71wITFbRVLrqJ6VqaCBI; um_auth=1; competition_session=MTc4MTY4NzU2MXxOd3dBTkVveVZGTlRSMUUwVGxCVldEWTJORlZSVUZKT1FWWlpTa3hQTjBGV1VVWkZWMFZRV1ZrM1MwVldSMFpHVGtKSlJFTmFOMUU9fANF_pFF9nf6PbM0hBMpcwaiQNtBV45eOp8q1bBzUY0P

{"answer":"flag{fbd0dd40-938e-4c25-ad5a-5a878f193a86}"}




HTTP/1.1 200 OK
Server: nginx
Date: Wed, 17 Jun 2026 09:25:46 GMT
Content-Type: application/json; charset=utf-8
Connection: keep-alive
Set-Cookie: competition_session=MTc4MTY4Nzg2MXxOd3dBTkVveVZGTlRSMUUwVGxCVldEWTJORlZSVUZKT1FWWlpTa3hQTjBGV1VVWkZWMFZRV1ZrM1MwVldSMFpHVGtKSlJFTmFOMUU9fNfImzGyrJ9YOaIMox2SLYtPigHDx49C3a-uKYUKN2zi; Path=/; Expires=Wed, 17 Jun 2026 11:17:41 GMT; Max-Age=7200
Content-Length: 37

{"data":null,"msg":"答案正确！"}
'''

import requests
from time import sleep
import logging
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# 精确屏蔽 InsecureRequestWarning 警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 配置参数
QUESTION_ID = "90122"


def upload_flag(flag_dict):
    """上传所有获取到的flag到竞赛平台"""
    url = f"https://172.19.6.100/competition/api/contestants/match_plan/{QUESTION_ID}/question/awd"
    headers = {
        "Host": "172.19.6.100",
        "Connection": "keep-alive",
        "sec-ch-ua-platform": "\"Windows\"",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "sec-ch-ua": "\"Google Chrome\";v=\"149\", \"Chromium\";v=\"149\", \"Not)A;Brand\";v=\"24\"",
        "Content-Type": "application/json",  # 关键：指定内容类型为 JSON
        "sec-ch-ua-mobile": "?0",
        "Origin": "https://172.19.6.100",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://172.19.6.100/competition_web/",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cookie": "um_auth=1; sso_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJVVUlEIjoiMjMzYWJiZjAtYzAzMS00MGQ4LWEzODctNDU5ODI5MGMyY2MzIiwiSUQiOjkwLCJVc2VybmFtZSI6InVzZXI4NiIsIk5pY2tOYW1lIjoidXNlcjg2IiwiSXNTdXBlciI6ZmFsc2UsIkxhc3RMb2dpbkF0IjoiMjAyNi0wNi0xOFQyMTowNDozNy4wNDM0NzYyOTQrMDg6MDAiLCJCdWZmZXJUaW1lIjowLCJpc3MiOiJxbVBsdXMiLCJuYmYiOjE3ODE3ODY4Nzd9.2P20iiNX9A7bTDaU1feQ2C7Cl-cND3pZbww9g8GchZA; competition_session=MTc4MTc4NzgwMnxOd3dBTkRjMU5GcE5WVmxYU3pORE4wY3lSa3RVTkVoYVJ6TkdWRmd5U0ZsSlRVNVlSRFZLU1VSS1NrOUNSMUZTTWxWR01sQkpTbEU9fGxfegurUX-usTdtd4GMFjfO8Uw5zY7ZPv33bKxYzckM",
    }
    # 忽略证书验证（内网自签名）
    session = requests.Session()
    session.verify = False
    with open("upload_res.txt", "w", encoding="utf-8") as f:
        f.write("提交flag失败\n")
    with open("upload_res.txt", "a", encoding="utf-8") as f:
        for ip, flag in flag_dict.items():
            if flag:
                payload = {"answer": flag}
                try:
                    resp = session.post(url, json=payload, headers=headers, timeout=5)
                    # 解析返回消息（假设返回json格式）
                    if resp.status_code == 200:
                        msg = resp.json().get("msg", "unknown")
                        logging.info(f"{ip} upload success: {msg}")
                    else:
                        msg = resp.json().get("msg", "unknown")
                        logging.error(f"{ip} upload failed, status {resp.status_code}, {msg}")
                        # 写入结果文件
                        f.write(f"{ip} upload failed, status {resp.status_code}  {msg} 写入失败，自行写入\n")
                except Exception as e:
                    logging.error(f"{ip} upload exception: {e}")
                    f.write(f"{ip} error, status {resp.status_code}  {msg} 写入失败，自行写入{flag}\n")
                sleep(20)
            else:
                pass


if __name__ == "__main__":
    flag_dict = {}
    with open("flag.txt", "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()  # 去除行首尾的空白字符和换行符
            if line:  # 确保不是空行
                key, value = line.split(":", 1)  # 使用 maxsplit=1 防止值中包含冒号被错误分割
                flag_dict[key.strip()] = value.strip()
    upload_flag(flag_dict)
