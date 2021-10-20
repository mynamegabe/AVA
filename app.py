from flask import Flask, render_template, make_response, request, redirect, url_for, session, send_from_directory
from threading import Thread
import threading

from main import base, tcp_scan, scan_thread

app = Flask(__name__, static_url_path='',static_folder='static')
app.secret_key = "0b3lUsK@5p3r5KY"

def web():
    app.run(host="0.0.0.0")


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/start', methods=['POST'])
def start():
    hostname = request.form['hostname']

    main_thread = Thread(target=base, args=[hostname])
    main_thread.start()

    web_thread.join()
    main_thread.join()

if __name__ == "__main__":
    web_thread = Thread(target=web)
    web_thread.start()