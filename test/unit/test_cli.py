import pytest

import ansiblediscover.cli as cli


@pytest.mark.parametrize('args, expected', [
    ('foo', ['foo']),
    ('foo bar baz', ['foo', 'bar', 'baz']),
    ('"foo bar" baz', ['foo bar', 'baz']),
    ('foo\\ bar baz', ['foo bar', 'baz']),
])
def test_split_shell_arguments(args, expected):
    assert expected == cli.split_shell_arguments(args)
