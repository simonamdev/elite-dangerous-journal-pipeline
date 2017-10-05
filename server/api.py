import time
from threading import Thread, Event

import rethinkdb as r

from flask import Flask, request, abort
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

debug_mode = True
api_header_name = 'API-KEY'
api_key = 'test'
if not debug_mode:
    api_key = 'bla'


thread = Thread()
thread_stop_event = Event()


class JournalEventReaderThread(Thread):
    def __init__(self):
        self.delay = 1
        super(JournalEventReaderThread, self).__init__()

    def read_changes(self):
        while not thread_stop_event.is_set():
            with get_connection() as conn:
                for change in r.table('authors').changes().run(conn):
                    print(change)
                    socketio.emit('journalEvent', change, namespace='/pipeline')
                    time.sleep(self.delay)

    def run(self):
        self.read_changes()


def get_connection():
    return r.connect(host='localhost', port=28015, db='test')


@app.before_request
def check_api_key():
    request_api_key = request.headers.get(api_header_name)
    if not api_key == request_api_key:
        abort(401)


"""
API Routes
"""


@app.route('/')
def index():
    return 'Hello'


@app.route('/event', methods=['POST'])
def receive_event():
    with get_connection() as conn:
        r.table('authors').insert(request.json).run(conn)
    return 'Inserted: {}'.format(request.json), 201


"""
Websocket Routes
"""


@socketio.on('connect', namespace='/pipeline')
def initialise_reader():
    global thread
    print('Client connected')
    if not thread.is_alive():
        print('Starting reader thread')
        thread = JournalEventReaderThread()
        thread.start()


@socketio.on('latency', namespace='/pipeline')
def latency_check(data):
    current_time = int(round(time.time() * 1000))
    # print('Client time: {}, Server time now: {}, Latency: {}ms'.format(data['timestamp'], current_time, current_time - data['timestamp']))
    emit('latencyResponse', {'timestamp': current_time, 'timestamp_client': data['timestamp']})


if __name__ == '__main__':
    socketio.run(app, debug=debug_mode)
    # app.run(debug=debug_mode)
