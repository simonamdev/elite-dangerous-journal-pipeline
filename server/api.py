import rethinkdb as r

from flask import Flask, request, abort
from flask_socketio import SocketIO, emit

app = Flask(__name__)
# socketio = SocketIO(app)

debug_mode = True
api_header_name = 'API-KEY'
api_key = 'test'
if not debug_mode:
    api_key = 'bla'


def get_connection():
    return r.connect(host='localhost', port=28015, db='test')


@app.before_request
def check_api_key():
    request_api_key = request.headers.get(api_header_name)
    if not api_key == request_api_key:
        abort(401)


@app.route('/')
def index():
    return 'Hello'


@app.route('/event', methods=['POST'])
def receive_event():
    with get_connection() as conn:
        r.table('authors').insert(request.json).run(conn)
    return 'Inserted: {}'.format(request.json), 201


if __name__ == '__main__':
    # socketio.run(app)
    app.run(debug=debug_mode)
