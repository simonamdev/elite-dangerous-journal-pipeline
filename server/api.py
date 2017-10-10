import time
import json
import rethinkdb as r

from threading import Thread, Event
from flask import Flask, request, abort
from flask import render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

api_header_name = 'API-KEY'

print('Reading Configuration file')
# Read in config values
with open('api_config.json', 'r') as config_file:
    config = json.loads(config_file.read())

debug_mode = config['debug']
db_name = config['database_name']
table_name = config['table_name']
api_key = 'test'
if not debug_mode:
    api_key = config[['api_key']]

thread = Thread()
thread_stop_event = Event()


class JournalEventReaderThread(Thread):
    def __init__(self):
        self.delay = 1
        super(JournalEventReaderThread, self).__init__()

    def read_changes(self):
        while not thread_stop_event.is_set():
            with get_connection() as conn:
                for change in r.table(table_name).changes().run(conn):
                    print(change)
                    socketio.emit('journalEvent', change, namespace='/pipeline')
                    time.sleep(self.delay)

    def run(self):
        self.read_changes()


def get_connection():
    return r.connect(host='localhost', port=28015, db=db_name)


def check_api_key():
    request_api_key = request.headers.get(api_header_name)
    if not api_key == request_api_key:
        abort(401)


"""
API Routes
"""


@app.route('/')
def index():
    return 'Index Page'


@app.route('/overlay')
def overlay():
    return render_template('overlay.min.html')


@app.route('/event', methods=['POST'])
def receive_event():
    check_api_key()
    with get_connection() as conn:
        r.table(table_name).insert(request.json).run(conn)
    return 'Inserted: {}'.format(request.json), 201


"""
Websocket Routes
"""


@socketio.on('latency', namespace='/pipeline')
def latency_check(data):
    current_time = int(round(time.time() * 1000))
    emit('latencyResponse', {'timestamp': current_time, 'timestamp_client': data['timestamp']})


if __name__ == '__main__':
    # Attempt to create the table
    with get_connection() as conn:
        try:
            r.db_create(db_name).run(conn)
            print('Created Database: {}'.format(db_name))
        except r.RqlRuntimeError:
            print('Database: {} already exist'.format(db_name))
        try:
            r.db(db_name).table_create(table_name).run(conn)
            print('Created Table: {}'.format(table_name))
        except r.RqlRuntimeError:
            print('Table: {} already exist'.format(table_name))
        finally:
            conn.close()
    if not thread.is_alive():
        print('Starting reader thread')
        thread = JournalEventReaderThread()
        thread.start()
    socketio.run(app, debug=debug_mode)
