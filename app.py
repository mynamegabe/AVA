from flask import Flask, render_template, make_response, request, redirect, url_for, session, send_from_directory
from threading import Thread
#from flask_socketio import SocketIO
from flask_cors import CORS, cross_origin
import socketio
import eventlet
from main import base, tcp_scan, scan_thread
import threading

app = Flask(__name__, static_url_path='',static_folder='static')
app.secret_key = "0b3lUsK@5p3r5KY"
app.config['CORS_HEADERS'] = 'Content-Type'
#socketio = SocketIO(app)

sio = socketio.Server(cors_allowed_origins='http://127.0.0.1:5000')
wsapp = socketio.WSGIApp(sio, static_files={
    '/': {'content_type': 'text/html', 'filename': 'index.html'}
})

def web():
    app.run(host="127.0.0.1")


@app.route('/')
@cross_origin()
def index():
    sio.emit('hellooooo')
    return render_template('index.html')


@app.route('/start', methods=['POST'])
@cross_origin()
def start():
    hostname = request.form['hostname']

    main_thread = Thread(target=base, args=[hostname])
    main_thread.start()


    return {'msg': 'Y'}

    #main_thread.join()


def websocket():
    eventlet.wsgi.server(eventlet.listen(('', 6001)), wsapp)

@sio.event
def connect(sid, environ):
    sio.send('hello')
    print("connect ", sid)

@sio.event
def my_message(sid, data):
    print('message ', data)

@sio.event
def sendmsg():
    threading.Timer(5.0, sendmsg).start()
    sio.emit('message',{'data': 'hello'})
    #print('l')


if __name__ == "__main__":
    sendmsg()

    web_thread = Thread(target=web)
    web_thread.start()

    ws = Thread(target=websocket)
    ws.start()