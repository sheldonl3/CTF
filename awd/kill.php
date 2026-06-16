<?php
//不死马删除脚本，修改unlink的不死马文件名，pid不用改，然后#php kill.php
while(1){
$pid=1234;
@unlink('1.php');
exec('kill -9 $pid');
}
?>