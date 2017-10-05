import Client from './client';

export default class DemoClient extends Client {
    constructor(url) {
        super(url);
        this.changeCount = 0;
    }

    setup() {
        super.setup();
        this.setupJournalEvents();
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
            // Scroll to the bottom of the row to follow new events
            window.scrollTo(0, document.body.scrollHeight);
        });
    }
}
