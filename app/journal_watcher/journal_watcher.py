import os
import time


def get_difference(a, b):
    s = set(a)
    return [x for x in b if x not in s]


def watch_file(file_path, delay=0.1):
    with open(file_path, 'r') as log_file:
        # Go to the end of the file
        log_file.seek(0, 2)
        while True:
            line = log_file.readline()
            if line and not line == '\n':
                yield line
            time.sleep(delay)


class JournalWatcher:
    def __init__(self, directory):
        self._directory = directory
        self._journal_files = []
        self._current_file = None

    def watch(self):
        pass

    def watch_for_new_journal_files(self):
        files = os.scandir(self._directory)
        if not sorted(files) == sorted(self._journal_files):

            print('New journal file detected: {}')


if __name__ == '__main__':
    watcher = JournalWatcher(directory='')
    watcher.watch()
