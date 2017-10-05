import os

import sys
from argparse import ArgumentParser

from gooey import Gooey

from pipeline_app import PipelineApp


@Gooey
def main():
    # Requirement for Pyinstaller
    # nonbuffered_stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)
    # sys.stdout = nonbuffered_stdout
    # Add arguments
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
