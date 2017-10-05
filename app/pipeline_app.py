import json
import requests
import os
import time


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
        self._directory = str(directory)
        self._watch_delay = watch_delay
        self._journal_files = os.listdir(self._directory)
        self._current_file_path = get_last_modified_file_path(self._directory)

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


headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}


class PipelineApp:
    def __init__(self, journal_directory, cmdr_name, team_name, api_key, url):
        self._journal_directory = journal_directory
        self._cmdr_name = cmdr_name
        self._team_name = team_name
        self._api_key = api_key
        self._url = url
        self._journal_watcher = JournalWatcher(directory=self._journal_directory)

    def run(self):
        headers['API-KEY'] = self._api_key
        event_url = self._url + '/event'
        while True:
            data = {
                'cmdr_name': self._cmdr_name,
                'team_name': self._team_name
            }
            for event in self._journal_watcher.watch_latest_file():
                print('Event detected: {}'.format(event))
                data['event'] = event
                try:
                    response = requests.post(url=event_url, data=json.dumps(data), headers=headers, timeout=2)
                    print('Response: {}'.format(response.status_code))
                except Exception as e:
                    print(e)


if __name__ == '__main__':
    app = PipelineApp(
        journal_directory='C:\\Users\Simon\Saved Games\Frontier Developments\Elite Dangerous',
        cmdr_name='purrcat',
        team_name='wotsit',
        api_key='test',
        url='http://edjp.purrcat.space'
    )
    app.run()
