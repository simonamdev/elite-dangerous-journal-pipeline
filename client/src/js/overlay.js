import DemoClient from './models/demo-client';

let client = new DemoClient('http://127.0.0.1:5000/pipeline');

client.setup();
client.checkLatency();

setInterval(() => {
    client.checkLatency();
}, 3000);
