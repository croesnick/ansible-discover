import pytest

from ansiblediscover.entity.playbook import Playbook, PlaybookFactory


def test_init():
    path = 'path/to/myplaybook.yml'
    pf = PlaybookFactory(path)
    assert path == pf.path


@pytest.mark.parametrize('path, expected_valid', [
    ('path/to/myplaybook.yml', True),
    ('path/to/something', False),
])
def test_is_valid(path, expected_valid):
    pf = PlaybookFactory(path)
    assert expected_valid == pf.is_valid()


def test_path():
    path = 'path/to/myplaybook.yml'
    pf = PlaybookFactory(path)
    assert path == pf.path


@pytest.mark.parametrize('path, expected_name', [
    ('path/to/myplaybook.yml', 'myplaybook'),
    ('path/to/something', None),
])
def test_name(path, expected_name):
    pf = PlaybookFactory(path)
    assert expected_name == pf.name


def test_typestring():
    assert 'playbook' == PlaybookFactory('irrelevant').typestring


def test_build_success(mocker):
    path = 'path/to/myplaybook.yml'

    mock_pb_build = mocker.patch('ansiblediscover.entity.playbook.Playbook.build')
    mock_pb_build.return_value = Playbook([], path)

    built_pb = PlaybookFactory(path).build()

    assert Playbook == type(built_pb)
    assert path == built_pb.path
    mock_pb_build.assert_called_with(path)


def test_build_failure(mocker):
    mock_pb_build = mocker.patch('ansiblediscover.entity.playbook.Playbook.build')
    mock_pb_build.side_effect = RuntimeError()

    assert PlaybookFactory('irrelevant').build() is None
    mock_pb_build.assert_called_with('irrelevant')
