
import socket

def check_port(host, port):
    try:
        # 创建一个socket对象
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            # 设置超时时间
            sock.settimeout(1)
            # 尝试连接到指定的主机和端口
            sock.connect((host, port))
            return True  # 如果连接成功，返回True
    except socket.error:
        # 如果连接失败，返回False
        return False

host = '156.239.238.67' #2201  40 * 3=120
for port in range(8800,8880):
    is_open = check_port(host, port)
    if "True" in str(is_open):
        ip = host+':'+str(port)
        print(host+':'+str(port))
        with open("./ip.txt", 'a', encoding='UTF-8') as f: 
            f.write(f"http://{ip}/\n")