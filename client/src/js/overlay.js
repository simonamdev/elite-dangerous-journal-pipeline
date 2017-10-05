import Client from './models/client';

let c = new Client('http://127.0.0.1:5000/pipeline');

c.setup();

setInterval(() => {
    c.emitJournalEvent({ data: 'test' });
}, 500);
