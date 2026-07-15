//gcc ./question_3.c

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>


int init_func(){
    setvbuf(stdin,0,2,0);
    setvbuf(stdout,0,2,0);
    setvbuf(stderr,0,2,0);
    return 0;
}


void read_n(char *buf,int n){
	for(int i=0,i<n,i++)
		if(read(0,buf[i],1)!=1) exit(1);
	if(buf[i] == '\n') break;
}


void who(){
	char name[0x30];
	puts("your name:");
	read(name,0x20);
	printf("welcome %s",name);
}

int main(){
	init_func();
	
	puts("input:");
	gets(a);  
	printf("%s",a);

    return 0;
}
