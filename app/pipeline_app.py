import json
import requests

from argparse import ArgumentParser
from gooey import Gooey

from app.journal_watcher.journal_watcher import JournalWatcher


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


@Gooey
def main():
    parser = ArgumentParser()
    parser.add_argument(
        '-dir',
        required=True,
        default='C:\\Users\Simon\Saved Games\Frontier Developments\Elite Dangerous',
        dest='directory',
        help='Journal Directory')
    parser.add_argument(
        '-cmdr',
        required=True,
        dest='cmdr',
        help='Commander Name')
    parser.add_argument(
        '-team',
        required=True,
        dest='team',
        help='Team Name')
    parser.add_argument(
        '-api-key',
        required=True,
        dest='api_key',
        help='API Key (Purrcat should have given you this)')
    parser.add_argument(
        '-url',
        required=True,
        dest='url',
        help='Server URL')
    args = parser.parse_args()
    pipeline_app = PipelineApp(
        journal_directory=args.directory,
        cmdr_name=args.cmdr,
        team_name=args.team,
        api_key=args.api_key,
        url=args.url
    )
    pipeline_app.run()


if __name__ == '__main__':
    main()
