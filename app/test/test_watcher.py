import os
import pytest

from app.journal_watcher.journal_watcher import get_difference, JournalWatcher


class TestListDifference:
    def test_passing_empty_lists_returns_empty_list(self):
        assert [] == get_difference([], [])

    def test_passing_objects_in_only_left_returns_empty_list(self):
        assert [] == get_difference(['one'], [])

    def test_passing_objects_in_only_right_returns_right_list(self):
        assert ['two'] == get_difference([], ['two'])

    def test_passing_same_objects_returns_empty_list(self):
        assert [] == get_difference(['foo'], ['foo'])

    @pytest.mark.parametrize('a,b,expected', [
        (['foo'], ['foo', 'bar'], ['bar']),
        (['foo'], ['bar'], ['bar']),
        (['foo', 'bar'], ['bar'], [])
    ])
    def test_passing_different_objects_returns_expected_value(self, a, b, expected):
        assert expected == get_difference(a, b)


class TestDirectoryWatcher:
    def test_new_file_appearing(self, tmpdir):
        p = tmpdir.join('file.txt')
        p.write('content')
        # Watcher started after file created
        watcher = JournalWatcher(directory=tmpdir)
        new_file = watcher.get_new_journal_file()
        assert None is new_file
        assert 1 == len(tmpdir.listdir())
        p = tmpdir.join('file-2.txt')
        p.write('new content')
        new_file = watcher.get_new_journal_file()
        assert 'file-2.txt' == new_file
        assert 2 == len(tmpdir.listdir())

    def test_file_deleting(self, tmpdir):
        p = tmpdir.join('file.txt')
        p.write('content')
        # Watcher started after file created
        watcher = JournalWatcher(directory=tmpdir)
        new_file = watcher.get_new_journal_file()
        assert None is new_file
        assert 1 == len(tmpdir.listdir())
        # delete the file
        os.remove(p)
        new_file = watcher.get_new_journal_file()
        assert None is new_file
        assert 0 == len(tmpdir.listdir())
