//gcc -static -o ret2syscall ret2syscall.c -no-pie -fno-stack-protector

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
char sh[]="/bin/sh";

int init_func(){
    setvbuf(stdin,0,2,0);
    setvbuf(stdout,0,2,0);
    setvbuf(stderr,0,2,0);
    return 0;
}


int main(){
	init_func();
	
	char a[8] = {};
	char b[8] = {};

	puts("input:");
	gets(a);  
	printf("%s",a);

    return 0;
}
