import os
import json
import time
import requests

from threading import Thread


def get_difference(a, b):
    s = set(a)
    return [x for x in b if x not in s]


def get_last_modified_file_path(directory):
    last_modified_files = sorted(
        [
            dict(file=file, timestamp=os.stat(os.path.join(str(directory), file)).st_mtime) for file in os.listdir(str(directory))
        ],
        key=lambda x: x['timestamp'],
        reverse=True
    )
    return os.path.join(str(directory), last_modified_files[0]['file'])


class JournalWatcher:
    def __init__(self, directory, watch_delay=0.1):
        self._directory = self._parse_journal_directory(directory=str(directory))
        self._watch_delay = watch_delay
        self._journal_files = os.listdir(self._directory)
        self._current_file_path = get_last_modified_file_path(self._directory)

    @staticmethod
    def _parse_journal_directory(directory):
        if 'USERPROFILE' in directory:
            return directory.replace('%USERPROFILE%', os.getenv('USERPROFILE'))
        return directory

    def watch_latest_file(self):
        print('Reading file at path: {}'.format(self._current_file_path))
        with open(self._current_file_path, 'r') as journal_file:
            # Go to the end of the file
            print('Seeking to the end of the journal file')
            journal_file.seek(0, 2)
            while True:
                new_file_path = self.get_new_journal_file()
                # stop looping if a new journal has been detected
                if new_file_path:
                    print('Switching to file: {}'.format(new_file_path))
                    self._current_file_path = new_file_path
                    break
                line = journal_file.readline()
                if line and not line == '\n':
                    yield line
                time.sleep(self._watch_delay)

    def get_new_journal_file(self):
        files = os.listdir(self._directory)
        if not sorted(files) == sorted(self._journal_files):
            new_files = get_difference(self._journal_files, files)
            # Update the files seen by the class
            self._journal_files = files
            # Checking the length takes deletions into consideration
            if len(new_files):
                new_file = new_files[0]
                print('New journal file detected: {}'.format(new_file))
                return new_file
        return None


class EventWhitelist:
    def __init__(self, file_path):
        self._file_path = file_path
        self._required_events = []
        self._validate_events_file()
        self._read_required_events_file()

    def _validate_events_file(self):
        if not os.path.isfile(self._file_path):
            raise FileNotFoundError('Events whitelist file is not at: {}'.format(self._file_path))

    def _read_required_events_file(self):
        with open(self._file_path, 'r') as events_file:
            for line in events_file:
                self._required_events.append(line.strip())
        if len(self._required_events) == 0:
            print('No white list provided, allow all events')
        print('White listing following events:')
        for event in self._required_events:
            print('> {}'.format(event))

    def get_required_events(self):
        return self._required_events


class PipelineApp:
    def __init__(self, journal_directory, events_required, cmdr_name, team_name, api_key, url):
        self._journal_directory = journal_directory
        self._events_required = events_required
        self._cmdr_name = cmdr_name
        self._team_name = team_name
        self._headers = {
            'Content-type': 'application/json',
            'Accept': 'text/plain',
            'API-KEY': api_key
        }
        self._url = url
        self._events_url = url + '/event'
        self._journal_watcher = JournalWatcher(directory=self._journal_directory)

    def run(self):
        while True:
            data = {
                'cmdr_name': self._cmdr_name,
                'team_name': self._team_name
            }
            for event in self._journal_watcher.watch_latest_file():
                event = json.loads(event)
                if event['event'] not in self._events_required and not len(self._events_required) == 0:
                    print('Skipping event: {}'.format(event['event']))
                    continue
                print('Event detected: {}'.format(event['event']))
                data['event'] = event
                try:
                    # response = requests.post(url=event_url, data=json.dumps(data), headers=headers, timeout=2)
                    Thread(target=self.send_event_to_api, args=[data, 2]).start()
                except Exception as e:
                    print(e)

    def send_event_to_api(self, post_data, timeout):
        response = requests.post(
            url=self._events_url,
            data=json.dumps(post_data),
            headers=self._headers,
            timeout=timeout
        )
        # print(response.text)
        return print('Response: {}'.format(response.status_code))


if __name__ == '__main__':
    if not os.path.isfile('config.json'):
        print('Config file not present')
        exit(-1)
    with open('config.json', 'r') as config_file:
        data = config_file.read()
    args = json.loads(data)
    events_required = EventWhitelist(file_path='events.txt').get_required_events()
    pipeline_app = PipelineApp(
        journal_directory=args['directory'],
        events_required=events_required,
        cmdr_name=args['cmdr'],
        team_name=args['team'],
        api_key=args['api_key'],
        url=args['url']
    )
    pipeline_app.run()
