	.file	"hello.c"
	.text
	.globl	div_by_10
	.type	div_by_10, @function
div_by_10:
.LFB0:
	.cfi_startproc
	endbr64
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	movl	%edi, -4(%rbp)
	movl	-4(%rbp), %eax
	movslq	%eax, %rdx
	imulq	$1717986919, %rdx, %rdx
	shrq	$32, %rdx
	sarl	$2, %edx
	sarl	$31, %eax
	subl	%eax, %edx
	movl	%edx, %eax
	popq	%rbp
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE0:
	.size	div_by_10, .-div_by_10
	.globl	mod_by_8
	.type	mod_by_8, @function
mod_by_8:
.LFB1:
	.cfi_startproc
	endbr64
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	movl	%edi, -4(%rbp)
	movl	-4(%rbp), %edx
	movl	%edx, %eax
	sarl	$31, %eax
	shrl	$29, %eax
	addl	%eax, %edx
	andl	$7, %edx
	subl	%eax, %edx
	movl	%edx, %eax
	popq	%rbp
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE1:
	.size	mod_by_8, .-mod_by_8
	.globl	sum_array
	.type	sum_array, @function
sum_array:
.LFB2:
	.cfi_startproc
	endbr64
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	movq	%rdi, -24(%rbp)
	movl	%esi, -28(%rbp)
	movl	$0, -8(%rbp)
	movl	$0, -4(%rbp)
	jmp	.L6
.L7:
	movl	-4(%rbp), %eax
	cltq
	leaq	0(,%rax,4), %rdx
	movq	-24(%rbp), %rax
	addq	%rdx, %rax
	movl	(%rax), %eax
	addl	%eax, -8(%rbp)
	addl	$1, -4(%rbp)
.L6:
	movl	-4(%rbp), %eax
	cmpl	-28(%rbp), %eax
	jl	.L7
	movl	-8(%rbp), %eax
	popq	%rbp
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE2:
	.size	sum_array, .-sum_array
	.globl	xor_encrypt
	.type	xor_encrypt, @function
xor_encrypt:
.LFB3:
	.cfi_startproc
	endbr64
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	movq	%rdi, -24(%rbp)
	movl	%esi, -28(%rbp)
	movl	%edx, %eax
	movb	%al, -32(%rbp)
	movl	$0, -4(%rbp)
	jmp	.L10
.L11:
	movl	-4(%rbp), %eax
	movslq	%eax, %rdx
	movq	-24(%rbp), %rax
	addq	%rdx, %rax
	movzbl	(%rax), %esi
	movzbl	-32(%rbp), %ecx
	movl	-4(%rbp), %eax
	movslq	%eax, %rdx
	movq	-24(%rbp), %rax
	addq	%rdx, %rax
	xorl	%ecx, %esi
	movl	%esi, %edx
	movb	%dl, (%rax)
	addl	$1, -4(%rbp)
.L10:
	movl	-4(%rbp), %eax
	cmpl	-28(%rbp), %eax
	jl	.L11
	nop
	nop
	popq	%rbp
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE3:
	.size	xor_encrypt, .-xor_encrypt
	.globl	rol32
	.type	rol32, @function
rol32:
.LFB4:
	.cfi_startproc
	endbr64
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	movl	%edi, -4(%rbp)
	movl	%esi, -8(%rbp)
	movl	-8(%rbp), %eax
	movl	-4(%rbp), %edx
	movl	%eax, %ecx
	roll	%cl, %edx
	movl	%edx, %eax
	popq	%rbp
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE4:
	.size	rol32, .-rol32
	.globl	max_of_three
	.type	max_of_three, @function
max_of_three:
.LFB5:
	.cfi_startproc
	endbr64
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	movl	%edi, -20(%rbp)
	movl	%esi, -24(%rbp)
	movl	%edx, -28(%rbp)
	movl	-20(%rbp), %eax
	movl	%eax, -4(%rbp)
	movl	-24(%rbp), %eax
	cmpl	-4(%rbp), %eax
	jle	.L15
	movl	-24(%rbp), %eax
	movl	%eax, -4(%rbp)
.L15:
	movl	-28(%rbp), %eax
	cmpl	-4(%rbp), %eax
	jle	.L16
	movl	-28(%rbp), %eax
	movl	%eax, -4(%rbp)
.L16:
	movl	-4(%rbp), %eax
	popq	%rbp
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE5:
	.size	max_of_three, .-max_of_three
	.section	.rodata
.LC0:
	.string	"admin"
.LC1:
	.string	"s3cr3t"
	.text
	.globl	check_admin
	.type	check_admin, @function
check_admin:
.LFB6:
	.cfi_startproc
	endbr64
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	subq	$16, %rsp
	movq	%rdi, -8(%rbp)
	movq	-8(%rbp), %rax
	addq	$4, %rax
	leaq	.LC0(%rip), %rdx
	movq	%rdx, %rsi
	movq	%rax, %rdi
	call	strcmp@PLT
	testl	%eax, %eax
	jne	.L19
	movq	-8(%rbp), %rax
	addq	$20, %rax
	leaq	.LC1(%rip), %rdx
	movq	%rdx, %rsi
	movq	%rax, %rdi
	call	strcmp@PLT
	testl	%eax, %eax
	jne	.L19
	movq	-8(%rbp), %rax
	movl	$1, 36(%rax)
	movl	$1, %eax
	jmp	.L20
.L19:
	movl	$0, %eax
.L20:
	leave
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE6:
	.size	check_admin, .-check_admin
	.section	.rodata
.LC2:
	.string	"Monday"
.LC3:
	.string	"Tuesday"
.LC4:
	.string	"Wednesday"
.LC5:
	.string	"Thursday"
.LC6:
	.string	"Friday"
.LC7:
	.string	"Saturday"
.LC8:
	.string	"Sunday"
.LC9:
	.string	"Unknown"
	.text
	.globl	day_name
	.type	day_name, @function
day_name:
.LFB7:
	.cfi_startproc
	endbr64
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	movl	%edi, -4(%rbp)
	cmpl	$7, -4(%rbp)
	ja	.L22
	movl	-4(%rbp), %eax
	leaq	0(,%rax,4), %rdx
	leaq	.L24(%rip), %rax
	movl	(%rdx,%rax), %eax
	cltq
	leaq	.L24(%rip), %rdx
	addq	%rdx, %rax
	notrack jmp	*%rax
	.section	.rodata
	.align 4
	.align 4
.L24:
	.long	.L22-.L24
	.long	.L30-.L24
	.long	.L29-.L24
	.long	.L28-.L24
	.long	.L27-.L24
	.long	.L26-.L24
	.long	.L25-.L24
	.long	.L23-.L24
	.text
.L30:
	leaq	.LC2(%rip), %rax
	jmp	.L31
.L29:
	leaq	.LC3(%rip), %rax
	jmp	.L31
.L28:
	leaq	.LC4(%rip), %rax
	jmp	.L31
.L27:
	leaq	.LC5(%rip), %rax
	jmp	.L31
.L26:
	leaq	.LC6(%rip), %rax
	jmp	.L31
.L25:
	leaq	.LC7(%rip), %rax
	jmp	.L31
.L23:
	leaq	.LC8(%rip), %rax
	jmp	.L31
.L22:
	leaq	.LC9(%rip), %rax
.L31:
	popq	%rbp
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE7:
	.size	day_name, .-day_name
	.section	.rodata
.LC10:
	.string	"Division demo: 100 / 10 = %d\n"
.LC11:
	.string	"Mod demo: 100 %% 8 = %d\n"
.LC12:
	.string	"Sum demo: %d\n"
.LC13:
	.string	"Max demo: %d\n"
.LC14:
	.string	"Day demo: %s\n"
.LC15:
	.string	"Before xor: %s\n"
.LC16:
	.string	"After xor:  "
.LC17:
	.string	"%02X "
.LC18:
	.string	"Login success, role = %d\n"
	.text
	.globl	main
	.type	main, @function
main:
.LFB8:
	.cfi_startproc
	endbr64
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	pushq	%rbx
	subq	$184, %rsp
	.cfi_offset 3, -24
	movq	%fs:40, %rax
	movq	%rax, -24(%rbp)
	xorl	%eax, %eax
	movl	$1, -176(%rbp)
	movl	$2, -172(%rbp)
	movl	$3, -168(%rbp)
	movl	$4, -164(%rbp)
	movl	$5, -160(%rbp)
	movl	$100, %edi
	call	div_by_10
	movl	%eax, %esi
	leaq	.LC10(%rip), %rax
	movq	%rax, %rdi
	movl	$0, %eax
	call	printf@PLT
	movl	$100, %edi
	call	mod_by_8
	movl	%eax, %esi
	leaq	.LC11(%rip), %rax
	movq	%rax, %rdi
	movl	$0, %eax
	call	printf@PLT
	leaq	-176(%rbp), %rax
	movl	$5, %esi
	movq	%rax, %rdi
	call	sum_array
	movl	%eax, %esi
	leaq	.LC12(%rip), %rax
	movq	%rax, %rdi
	movl	$0, %eax
	call	printf@PLT
	movl	$5, %edx
	movl	$7, %esi
	movl	$3, %edi
	call	max_of_three
	movl	%eax, %esi
	leaq	.LC13(%rip), %rax
	movq	%rax, %rdi
	movl	$0, %eax
	call	printf@PLT
	movl	$3, %edi
	call	day_name
	movq	%rax, %rsi
	leaq	.LC14(%rip), %rax
	movq	%rax, %rdi
	movl	$0, %eax
	call	printf@PLT
	leaq	-96(%rbp), %rax
	movabsq	$6071801654790612296, %rcx
	movabsq	$8318823020887170886, %rbx
	movq	%rcx, (%rax)
	movq	%rbx, 8(%rax)
	movw	$101, 16(%rax)
	leaq	-96(%rbp), %rax
	movq	%rax, %rsi
	leaq	.LC15(%rip), %rax
	movq	%rax, %rdi
	movl	$0, %eax
	call	printf@PLT
	leaq	-96(%rbp), %rax
	movq	%rax, %rdi
	call	strlen@PLT
	movl	%eax, %ecx
	leaq	-96(%rbp), %rax
	movl	$55, %edx
	movl	%ecx, %esi
	movq	%rax, %rdi
	call	xor_encrypt
	leaq	.LC16(%rip), %rax
	movq	%rax, %rdi
	movl	$0, %eax
	call	printf@PLT
	movl	$0, -180(%rbp)
	jmp	.L33
.L34:
	movl	-180(%rbp), %eax
	cltq
	movzbl	-96(%rbp,%rax), %eax
	movzbl	%al, %eax
	movl	%eax, %esi
	leaq	.LC17(%rip), %rax
	movq	%rax, %rdi
	movl	$0, %eax
	call	printf@PLT
	addl	$1, -180(%rbp)
.L33:
	movl	-180(%rbp), %eax
	movslq	%eax, %rbx
	leaq	-96(%rbp), %rax
	movq	%rax, %rdi
	call	strlen@PLT
	cmpq	%rax, %rbx
	jb	.L34
	movl	$10, %edi
	call	putchar@PLT
	movl	$1, -144(%rbp)
	movabsq	$474215179361, %rax
	movl	$0, %edx
	movq	%rax, -140(%rbp)
	movq	%rdx, -132(%rbp)
	movabsq	$127764311257971, %rax
	movl	$0, %edx
	movq	%rax, -124(%rbp)
	movq	%rdx, -116(%rbp)
	movl	$0, -108(%rbp)
	leaq	-144(%rbp), %rax
	movq	%rax, %rdi
	call	check_admin
	testl	%eax, %eax
	je	.L35
	movl	-108(%rbp), %eax
	movl	%eax, %esi
	leaq	.LC18(%rip), %rax
	movq	%rax, %rdi
	movl	$0, %eax
	call	printf@PLT
.L35:
	movl	$0, %eax
	movq	-24(%rbp), %rdx
	subq	%fs:40, %rdx
	je	.L37
	call	__stack_chk_fail@PLT
.L37:
	movq	-8(%rbp), %rbx
	leave
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE8:
	.size	main, .-main
	.ident	"GCC: (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0"
	.section	.note.GNU-stack,"",@progbits
	.section	.note.gnu.property,"a"
	.align 8
	.long	1f - 0f
	.long	4f - 1f
	.long	5
0:
	.string	"GNU"
1:
	.align 8
	.long	0xc0000002
	.long	3f - 2f
2:
	.long	0x3
3:
	.align 8
4:
