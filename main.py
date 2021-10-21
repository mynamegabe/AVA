import socket, sys, threading
from queue import Queue
import socketio
import requests

sio = socketio.Client()
print_lock = threading.Lock()
q = Queue()
portlist = []
complete = False

@sio.event
def connect():
    print("I'm connected!")

@sio.event
def message(data): #send ports
    global complete
    if complete == False:
        sio.send({'type':'data', 'content-type': 'ports', 'content':portlist})
        complete = True
    else:
        sio.disconnect()

def scan_thread(ip):
    while True:
        port = q.get()
        p = tcp_scan(ip, port)
        if p:
            portlist.append(p)
        q.task_done()

def tcp_scan(ip,p):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        result = s.connect_ex((ip,p))
        if result == 0:
            return p
        s.close()
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

    port_range = 100

    if addr_valid:
        for _ in range(port_range):
            t = threading.Thread(target=scan_thread, args=[addr])
            t.daemon = True
            t.start()

        for p in range(port_range):
            q.put(p)

        q.join()
        sio.connect('http://127.0.0.1:6001')