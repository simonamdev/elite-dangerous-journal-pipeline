import io from 'socket.io-client';

// Init the socket
let socket = io('http://localhost:5000/test');

// Setup the socket
socket.on('connect_failed', () => {
    socket.close();
});

socket.on('disconnect', () => {
    socket.close();
});

socket.on('connect', () => {
    socket.emit('my event', { data: 'hello' });
    socket.on('my response', (res) => {
        console.log(res);
    });
});
