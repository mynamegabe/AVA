import socketio
import requests
sio = socketio.Client()

portlist = [1,2,3]
count = 0

@sio.event
def connect():
    print("I'm connected!")

@sio.event
def message(data): #send ports
    global count
    if count == 0:
        sio.send({'type':'data', 'content':portlist})
    else:
        sio.disconnect()
    count += 1

sio.connect('http://127.0.0.1:5999')
