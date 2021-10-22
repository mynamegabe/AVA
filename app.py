from flask import Flask, render_template, make_response, request, redirect, url_for, session, send_from_directory
from threading import Thread
from flask_cors import CORS, cross_origin
import socketio
import eventlet
from main import base, tcp_scan, scan_thread
import threading
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration
from datetime import datetime

app = Flask(__name__, static_url_path='',static_folder='static')
app.secret_key = "0b3lUsK@5p3r5KY"
app.config['CORS_HEADERS'] = 'Content-Type'


def web():
    app.run(host="127.0.0.1")


@app.route('/')
@cross_origin()
def index():
    return render_template('index.html')


@app.route('/start', methods=['POST'])
@cross_origin()
def start():
    hostname = request.form['hostname']
    main_thread = Thread(target=base, args=[hostname]).start()
    return {'msg': 'Y'}

    #main_thread.join()


def generate_pdf():
    now = datetime.now()
    font_config = FontConfiguration()
    html = HTML(string=f'<h1>Vulnerability Assessment</h1>\n\
                       <h3>{now}</h3>')
    css = CSS(string='''
        @font-face {
            font-family: Gentium;
            src: url(http://example.com/fonts/Gentium.otf);
        }
        h1 { font-family: Gentium }''', font_config=font_config)
    html.write_pdf(
        'report.pdf', stylesheets=[css],
        font_config=font_config)

if __name__ == "__main__":
    #sendmsg()

    web_thread = Thread(target=web)
    web_thread.start()

    generate_pdf()