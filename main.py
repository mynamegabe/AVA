import socket, sys, threading
from queue import Queue
import socketio
import nmap
import os
import re

sio = socketio.Client()
print_lock = threading.Lock()
q = Queue()
portlist = []
complete = False
mode = "nmap"  # nmap or tcp

@sio.event
def connect():
    print("I'm connected!")

@sio.event
def message(data): #send ports
    global complete
    if complete == False:
        if mode == "tcp":
            sio.send({'type':'data', 'content-type': 'ports', 'content':portlist})
        elif mode == "nmap":
            with open('temp.xml','r') as r:
                content  = r.read()
                r.close()
            print(content)
            ports1 = re.findall(r'portid=\"[\d]*\"',content)
            ports = []
            print(ports1)
            for i in ports1:
                ports.append(re.findall(r'\d+',i)[0])
            content2 = os.popen('searchsploit --nmap temp.xml').read()
            os.remove('temp.xml')
            sio.send({'type': 'data', 'content-type': 'nmap,searchsploit', 'content': [ports,content2]})
            with open('report.html','a') as w:
                addHtml = f"<p style='page-break-before: always' ></p><h3>Port scan</h3>"
                for port in ports:
                    addHtml += f"<h5>Port {port} open</h5>"
                
                addHtml += "<br><h3>Searchsploit results</h3>" + content2
                
                w.write(addHtml)
                w.close()
        complete = True
        print("Ports sent")
        
        
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


def nmap_scan(ip,p):
    nm = nmap.PortScanner()
    print("Nmap scan started")
    nm.scan(ip, p, arguments="-sV")
    xmlOut = nm.get_nmap_last_output()
    with open("temp.xml", "w") as results:
        results.write(xmlOut.decode())
        results.close()
    print("Nmap scan completed")


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

    port_range = "100"  # for tcp scan
    port_range = "0-80"  # for nmap scan

    if addr_valid:
        if mode == "tcp":
            # tcp scan
            for _ in range(port_range):
                t = threading.Thread(target=scan_thread, args=[addr])
                t.daemon = True
                t.start()

            for p in range(port_range):
                q.put(p)

            q.join()
        elif mode == "nmap":
            nmap_scan(addr, port_range)
            
        with open('report.html','a') as w:
            addHtml = f"<h3>IP Address:{addr}</h3><h3>Ports scanned: {port_range}</h3>"
            w.write(addHtml)
            w.close()
            
        sio.connect('http://127.0.0.1:6001')
