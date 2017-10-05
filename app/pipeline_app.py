import json
import requests

from .journal_watcher.journal_watcher import JournalWatcher

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
