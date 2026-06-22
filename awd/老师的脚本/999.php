<?php 
//一键部署通发
system('chmod 777 TZYLY.php ');
system('php TZYLY.php --install /var/www/html');
system('chmod 777 xing.php');
?>