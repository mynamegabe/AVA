from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
sio = SocketIO(app, cors_allowed_origins="http://127.0.0.1:5000")

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
        if msg['type'] == 'data':
            data['content'] = msg['content']
            s = True
            print("Received")
        elif msg['type'] == 'wait' and s:
            sio.send(data)
            print("Sent")
            s = False


if __name__ == '__main__':
    sio.run(app, host="0.0.0.0", port=6001)
