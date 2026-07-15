/*
 * CTF 逆向培训演示用 —— 编译过程与优化级别对比
 *
 * 查看各阶段产物:
 *   gcc -E hello.c -o hello.i          # 预处理
 # extern 只是声明这个外部函数，具体实现是最后链接过程去找
 *   gcc -S -O0 hello.c -o hello_O0.s   # 编译为汇编
 *   gcc -S -O2 hello.c -o hello_O2.s   # 对比 O2 的汇编差异
 *   gcc -c hello.c -o hello.o          # 汇编为目标文件
 *   gcc hello.o -o hello               # 链接
 #  动态链接至少包含两个内容：
        ld 连接器，将所有目标文件和标准库组成完整的可执行文件
        libc 标准C库
  * 编译命令:
 *   gcc -O0 -o hello_O0 hello.c        # 无优化，变量均在栈上
 *   gcc -O1 -o hello_O1 hello.c        # 基础优化
 *   gcc -O2 -o hello_O2 hello.c        # 标准优化
 *   gcc -O3 -o hello_O3 hello.c        # 激进优化
 *
 * 用 IDA 分别打开 hello_O0 和 hello_O2，对比反编译结果，
 * 观察编译优化对逆向分析的影响。
 */

#include <stdio.h>
#include <string.h>
#include <stdint.h>

#define MAGIC 0x37
#define MAX_LEN 64

/* == 除法/取模 → 观察 O2 如何优化为乘法和位运算 == */
int div_by_10(int n) {
    return n / 10;
}

int mod_by_8(int n) {
    return n % 8;
}

/* == 循环 → 观察 O2 的循环展开、寄存器分配 == */
int sum_array(int *arr, int len) {
    int sum = 0;
    for (int i = 0; i < len; i++) {
        sum += arr[i];
    }
    return sum;
}

/* == 简单 XOR 加密 → 在 IDA 中练习算法识别 == */
void xor_encrypt(char *data, int len, uint8_t key) {
    for (int i = 0; i < len; i++) {
        data[i] ^= key;
    }
}

/* == 循环左移 → 观察 (x<<n)|(x>>(32-n)) 模式 == */
uint32_t rol32(uint32_t val, int n) {
    return (val << n) | (val >> (32 - n));
}

/* == 条件分支 → 观察 O2 的 cmov 优化 == */
int max_of_three(int a, int b, int c) {
    int max = a;
    if (b > max) max = b;
    if (c > max) max = c;
    return max;
}

/* == 结构体 → 观察成员偏移访问 == */
struct Credential {
    int   id;
    char  name[16];
    char  pass[16];
    int   role;
};

int check_admin(struct Credential *cred) {
    if (strcmp(cred->name, "admin") == 0 &&
        strcmp(cred->pass, "s3cr3t") == 0) {
        cred->role = 1;
        return 1;
    }
    return 0;
}

/* == switch → 观察跳转表 == */
const char *day_name(int n) {
    switch (n) {
        case 1: return "Monday";
        case 2: return "Tuesday";
        case 3: return "Wednesday";
        case 4: return "Thursday";
        case 5: return "Friday";
        case 6: return "Saturday";
        case 7: return "Sunday";
        default: return "Unknown";
    }
}

/* == main 入口 == */
int main() {
    char buf[MAX_LEN];
    int  arr[] = {1, 2, 3, 4, 5};

    printf("Division demo: 100 / 10 = %d\n", div_by_10(100));
    printf("Mod demo: 100 %% 8 = %d\n", mod_by_8(100));
    printf("Sum demo: %d\n", sum_array(arr, 5));
    printf("Max demo: %d\n", max_of_three(3, 7, 5));
    printf("Day demo: %s\n", day_name(3));

    strcpy(buf, "Hello_CTF_Reverse");
    printf("Before xor: %s\n", buf);
    xor_encrypt(buf, strlen(buf), MAGIC);
    printf("After xor:  ");
    for (int i = 0; i < strlen(buf); i++) printf("%02X ", (unsigned char)buf[i]);
    printf("\n");

    struct Credential cred = {1, "admin", "s3cr3t", 0};
    if (check_admin(&cred)) {
        printf("Login success, role = %d\n", cred.role);
    }

    return 0;
}
