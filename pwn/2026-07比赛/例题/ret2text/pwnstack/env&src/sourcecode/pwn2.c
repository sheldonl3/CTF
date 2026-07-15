// gcc pwn2.c -fno-stack-protector -o pwn2
#include <stdio.h>
int initsetbuf()
{   

    setvbuf(stdin, 0LL, 2, 0LL);
    setvbuf(stdout, 0LL, 2, 0LL);
    setvbuf(stderr, 0LL, 2, 0LL);
    return 0;
}

int vuln()
{
	char str[0xa0]={0};
	read(0,str,0xb1);
	return 0;
}
int backdoor()
{
	system("/bin/sh\x00");
}
int main()
{
	puts("this is pwn1,can you do that??");
	vuln();
	return 0;

}