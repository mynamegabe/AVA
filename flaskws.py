from flask import Flask, render_template
from flask_socketio import SocketIO
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
sio = SocketIO(app, cors_allowed_origins="*")

data = {'type': 'data', 'content': ''}
s = False


@sio.on('connect')
def handleconnect(sid="",environ=""):
    sio.send('hello', broadcast=True)
    print("connect ", sid)


@sio.on('message')
def handlemsg(msg):
    global s
    print(msg, type(msg))
    if type(msg) == str:
        pass
        # print(msg)
    else:
        if 'content-type' in msg:
            data['content-type'] = msg['content-type']
        if msg['type'] == 'data':
            data['content'] = msg['content']
            s = True
            print("Received")
        elif msg['type'] == 'readfile': #unused
            with open(msg['filename'],'r') as r:
                data['content'] = r.read()
                s = True
                print("Received")
                r.close()
            os.remove(msg['filename'])
        elif msg['type'] == 'wait' and s:
            sio.send(data)
            print("Sent")

            s = False


if __name__ == '__main__':
    sio.run(app, host="0.0.0.0", port=6001)
