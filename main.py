import socket, sys, threading
from queue import Queue

print_lock = threading.Lock()
q = Queue()

def scan_thread(ip, port):
    while True:
        port = q.get()
        tcp_scan(ip, port)
        q.task_done()

def tcp_scan(ip,p):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        result = socket.connect_ex((ip,p))
        if result == 0:
            print(f"port {p}")
        sock.close()
    except socket.error:
        print("Machine could not be reached")
        sys.exit()
    except KeyboardInterrupt:
        print('Exiting...')
        sys.exit()

def base(addr):
    addr_valid = True
    try:
        socket.inet_aton(addr)
    except socket.error:
        try:
            addr = socket.gethostbyname(addr)
        except socket.gaierror:
            addr_valid = False
            print("Hostname not resolved")

    port_range = 80

    if addr_valid:
        for _ in range(port_range):
            t = threading.Thread(target=scan_thread, args=[addr])
            t.daemon = True
            t.start()

        for p in range(port_range):
            q.put(p)

        q.join()