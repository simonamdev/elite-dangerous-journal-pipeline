import time


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

    def watch(self):
        pass


if __name__ == '__main__':
    watcher = JournalWatcher(directory='')
    watcher.watch()
