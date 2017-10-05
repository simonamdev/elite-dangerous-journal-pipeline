import pytest

from app.journal_watcher.journal_watcher import get_difference


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
