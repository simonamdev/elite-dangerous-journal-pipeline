import io from 'socket.io-client';

export default class Client {
    constructor(url) {
        this.url = url;
        this.socket = io(url);
        this.changeCount = 0;
    }

    setup() {
        this.setupConnectionEvents();
        this.setupHealthEvents();
        this.setupJournalEvents();
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

    setupJournalEvents() {
        this.socket.on('journalEvent', (data) => {
            console.log(data);
            data = data['new_val']
            this.changeCount += 1;
            // Increase the change counter
            document.getElementById('changeCount').innerText = this.changeCount;
            // Add the change under the respective div if it exists
            let eventRowEl = document.createElement('div');
            let teamEl = document.createElement('h2');
            teamEl.innerText = data['team_name'];
            let cmdrEl = document.createElement('h3');
            cmdrEl.innerText = data['cmdr_name'];
            let dataEl = document.createElement('p');
            dataEl.innerText = JSON.stringify(data['event']);
            let horizontalRuleEl = document.createElement('hr');

            eventRowEl.appendChild(teamEl);
            eventRowEl.appendChild(cmdrEl);
            eventRowEl.appendChild(dataEl);
            eventRowEl.appendChild(horizontalRuleEl);
            document.getElementById('changes').appendChild(eventRowEl);
            window.scrollTo(0, document.body.scrollHeight);
        });
    }

    close() {
        this.socket.close();
    }

    checkLatency() {
        let timeNow = new Date().getTime();
        this.socket.emit('latency', { timestamp: timeNow });
    }

    emitJournalEvent(data) {
        this.socket.emit('journalEvent', data);
    }
}
