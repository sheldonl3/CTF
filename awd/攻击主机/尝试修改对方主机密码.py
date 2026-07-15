from concurrent.futures import ThreadPoolExecutor, as_completed
import paramiko
import time


def change_password_via_shell(hostname):
    """
    通过交互式 Shell 修改当前登录用户的密码
    """
    port = 22
    username = 'ctf'
    old_password = 'ctf'
    new_password = 'HLdf@2731'
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        # 1. 建立 SSH 连接
        print(f"正在连接 {hostname}...")
        client.connect(hostname=hostname, port=port, username=username, password=old_password)
        print("连接成功。")

        # 2. 启动交互式 Shell
        shell = client.invoke_shell()
        time.sleep(2)  # 等待 Shell 初始化

        # 清空初始缓冲区内容（如欢迎信息）
        if shell.recv_ready():
            shell.recv(4096)

        # 3. 发送 passwd 命令
        print(hostname+"执行 passwd 命令...")
        shell.send('passwd\n')
        time.sleep(2)

        # 读取提示符，确认进入密码修改流程
        output = shell.recv(4096).decode('utf-8', errors='ignore')
        print(f"系统提示: {output.strip()}")

        # 4. 输入旧密码
        # 注意：不同系统提示语可能不同，如 "Current password:" 或 "(current) UNIX password:"
        shell.send(old_password + '\n')
        time.sleep(2)

        # 5. 输入新密码
        shell.send(new_password + '\n')
        time.sleep(2)

        # 6. 再次输入新密码以确认
        shell.send(new_password + '\n')
        time.sleep(2)

        # 7. 获取最终结果
        final_output = shell.recv(4096).decode('utf-8', errors='ignore')
        print(f"执行结果:\n{final_output}")

        # 简单判断是否成功
        if "password updated successfully" in final_output.lower() or "successfully" in final_output.lower():
            print(hostname, "✅ 密码修改成功！")
            return hostname

            return True
        elif "bad password" in final_output.lower() or "error" in final_output.lower():
            print("❌ 密码修改失败：可能是密码复杂度不符合要求或旧密码错误。")
            return False
        else:
            print("⚠️ 未检测到明确的成功/失败消息，请检查上方输出。")
            return False

    except paramiko.AuthenticationException:
        print("❌ 认证失败：用户名或旧密码错误。")
        return False
    except Exception as e:
        print(f"❌ 发生错误: {str(e)}")
        return False
    finally:
        client.close()


if __name__ == "__main__":
    iplist = []
    res = []
    with open('ip.txt', 'r', encoding='utf-8') as file:
        # 逐行读取
        line = file.readline()
        # 循环直到文件末尾
        while line:
            # 将读取的行添加到列表中，移除行尾的换行符
            iplist.append(line.strip())
            # 读取下一行
            line = file.readline()

    with ThreadPoolExecutor(max_workers=30) as executor:
        futures = {executor.submit(change_password_via_shell, ip): ip for ip in iplist}
        for future in as_completed(futures):
            if future.result():
                res.append(future.result())
    with open('改密码结果.txt', 'w', encoding='utf-8') as file:
        for each in res:
            file.write(each + '\n')
