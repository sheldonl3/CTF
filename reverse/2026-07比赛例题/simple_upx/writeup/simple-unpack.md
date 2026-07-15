# Simple unpack



## **[目标]**
脱壳

## **[环境]**

kali

## **[工具]**
IDA, UPX

## **[分析过程]**

-  winhex打开后发现为upx壳

![image-20220411174045058](image/image-20220411174045058.png)

-  upx -d 脱壳后IDA打开即可看到flag

Then get the flag

![image-20220411174102092](image/image-20220411174102092.png)

```
flag{Upx_1s_n0t_a_d3liv3r_c0mp4ny}
```

