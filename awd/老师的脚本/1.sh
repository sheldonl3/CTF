#!/bin/bash
#一键启动前期部署工作

password="root"
# 使用passwd命令修改密码
echo -e "$password\n$password" | passwd "$USER" >/dev/null 2>&1

# 检查密码是否成功修改
if [ $? -eq 0 ]; then
    echo "修改密码成功"
else
    echo "修改密码失败"
fi
#备份整站
cd /var/www/html && tar -czvf /tmp/html.tgz ../html
echo "已成功备份到/tmp目录下"
chmod 777 ZZYLG.php
php TZYLY.php --install /var/www/html
echo "waf已启动"
chmod 777 xing.php
echo "正在监控一分钟之内新增并删除"
php xing.php


