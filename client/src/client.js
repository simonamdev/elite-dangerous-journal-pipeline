import io from 'socket.io-client';

// Init the socket
let socket = io();

// Setup the socket
socket.on('connect_failed', () => {
    socket.close();
});

socket.on('disconnect', () => {
    socket.close();
});
