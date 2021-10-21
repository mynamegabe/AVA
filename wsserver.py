import socketio
import requests
import eventlet

sio = socketio.Server(cors_allowed_origins='http://127.0.0.1:5000')
wsapp = socketio.WSGIApp(sio, static_files={
    '/': {'content_type': 'text/html', 'filename': 'index.html'}
})


@sio.on('connect')
def handleconnect(sid, environ):
    sio.send('hello',broadcast=True)
    print("connect ", sid)

@sio.on('message')
def handlemsg(sid,msg):
    print(msg)
    sio.send('hello')

eventlet.wsgi.server(eventlet.listen(('', 5999)), wsapp)
