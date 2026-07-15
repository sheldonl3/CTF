# Open-source


## **[目标]**


## **[环境]**

无

## **[工具]**
dev-c++

## **[分析过程]**

题目源码如下

```c++
#include <stdio.h>
#include <string.h>

int main(int argc, char *argv[]) {//外部调用输入参数
    if (argc != 4) {//输入三个参数，因为第一个是程序自己的名称
    	printf("what?\n");
    	exit(1);
    }

    unsigned int first = atoi(argv[1]);
    if (first != 0xcafe) {//第一个参数的十六进制为0xcafe
    	printf("you are wrong, sorry.\n");
    	exit(2);
    }

    unsigned int second = atoi(argv[2]);
    if (second % 5 == 3 || second % 17 != 8) {//第二个参数满足条件我口算有42，余数是不足才补的数，不是整除后剩的数。
    	printf("ha, you won't get it!\n");
    	exit(3);
    }

    if (strcmp("h4cky0u", argv[3])) {//第三个参数直接就是h4cky0u
    	printf("so close, dude!\n");
    	exit(4);
    }

    printf("Brr wrrr grr\n");

    unsigned int hash = first * 31337 + (second % 17) * 11 + strlen(argv[3]) - 1615810207;//这里的结果hash与前面输入参数有关，鄙人不才，曾一度想修改源码不输入参数直接输出这句话，当然，没有参数的这句话就会报错。

    printf("Get your key: ");
    printf("%x\n", hash);
    return 0;
}

```

- 通过分析源码得到3个参数分别为``51966``, `25`,`h4cky0u`.
第一个参数：0xcafe的十进制51966
第二个参数：满足second % 5 != 3  &&  second % 17 == 8  ->  25
第三个参数：strcmp("h4cky0u", argv[3]  -> h4cky0u

```Shell
% ./code 51966 25 h4cky0u
Brr wrrr grr
Get your key: c0ffee
```

flag{c0ffee}
