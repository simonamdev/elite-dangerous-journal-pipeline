import rethinkdb as r

from flask import Flask, request, abort
from flask_socketio import SocketIO, emit

app = Flask(__name__)
# socketio = SocketIO(app)


@app.route('/')
def index():
    return 'Hello'


@app.route('/event', methods=['POST'])
def receive_event():
    print(request.json)
    print(type(request.json))
    return '', 201


if __name__ == '__main__':
    # socketio.run(app)
    app.run(debug=True)
