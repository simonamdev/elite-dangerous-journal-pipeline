import io from 'socket.io-client';

export default class Client {
    constructor(url) {
        this.url = url;
        this.socket = io(url);
    }

    setup() {
        this.setupConnectionEvents();
        this.setupHealthEvents();
    }

    setupConnectionEvents() {
        this.socket.on('error', () => {
            console.log('Error');
        });

        this.socket.on('connect_failed', () => {
            console.log('Unable to connect');
            // this.close();
        });

        this.socket.on('disconnect', () => {
            console.log('Disconnecting');
            this.close();
        });

        this.socket.on('reconnecting', () => {
            console.log('Attempting to reconnect');
        });

        this.socket.on('reconnect_failed', () => {
            console.log('Unable to reconnect');
        });
    }

    setupHealthEvents() {
        this.socket.on('latencyResponse', (response) => {
            let requestTime = response['timestamp_client'];
            let serverTime = response['timestamp'];
            let latency = serverTime - requestTime;
            // console.log(`Time sent: ${requestTime}, Time received: ${serverTime}, Latency: ${latency}ms`);
            document.getElementById('latency').innerText = latency;
        });
    }

    checkLatency() {
        let timeNow = new Date().getTime();
        this.socket.emit('latency', { timestamp: timeNow });
    }

    close() {
        this.socket.close();
    }
}
