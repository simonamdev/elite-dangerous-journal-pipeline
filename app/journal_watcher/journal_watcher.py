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
        self._journal_files = os.listdir(directory)
        self._current_file = None

    def watch(self):
        pass

    def get_new_journal_file(self):
        files = os.listdir(self._directory)
        print(files)
        print(self._journal_files)
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


if __name__ == '__main__':
    watcher = JournalWatcher(directory='C:\\test')
    while True:
        watcher.get_new_journal_file()
        time.sleep(1)
