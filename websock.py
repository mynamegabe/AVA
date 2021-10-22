import socketio
import eventlet

sio = socketio.Server(cors_allowed_origins='http://127.0.0.1:5000')
wsapp = socketio.WSGIApp(sio, static_files={
    '/': {'content_type': 'text/html', 'filename': 'index.html'}
})

data = {'type': 'data', 'content': ''}
s = False


@sio.on('connect')
def handleconnect(sid, environ):
    sio.send('hello', broadcast=True)
    print("connect ", sid)


@sio.on('message')
def handlemsg(sid, msg):
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
    eventlet.wsgi.server(eventlet.listen(('', 6001)), wsapp)

