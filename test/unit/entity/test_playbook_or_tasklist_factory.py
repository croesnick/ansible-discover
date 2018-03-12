import os

import pytest
from ruamel import yaml

from ansiblediscover.entity.playbook import Playbook, PlaybookOrTasklistFactory


def test_init():
    path = os.path.join('path', 'to', 'my', 'playbook.yml')
    entity = PlaybookOrTasklistFactory(path)

    assert path == entity.path


@pytest.mark.parametrize('path, content, expected_validity', [
    (os.path.join('path', 'to', 'tasklist.yml'), None, True),
    (os.path.join('path', 'to', 'file'), None, False),
    (os.path.join('path', 'to', 'tasklist.yml'), [], True),
    (os.path.join('path', 'to', 'tasklist.yml'), [{'debug': {'msg': 'foo'}}], True),
    (os.path.join('path', 'to', 'pb.yml'), [{'hosts': 'all'}], True),
])
def test_is_valid(tmpdir, path, content, expected_validity):
    file_path = tmpdir.join(path)
    file_path.ensure(file=True)
    file_path.write(yaml.dump(content))

    entity = PlaybookOrTasklistFactory(str(file_path))

    assert expected_validity == entity.is_valid()


@pytest.mark.parametrize('content, expected', [
    (None, []),
    ([], []),
    ([{}], [{}]),
    ([{'debug': {'msg': 'foobar'}}], [{'debug': {'msg': 'foobar'}}]),
])
def test_data_success(tmpdir, content, expected):
    path = 'entity.yml'

    file_path = tmpdir.join(path)
    file_path.write(yaml.dump(content))

    entity = PlaybookOrTasklistFactory(str(file_path))

    assert expected == entity.data


def test_data_file_missing(tmpdir):
    file_path = tmpdir.join('missing.yml')
    entity = PlaybookOrTasklistFactory(str(file_path))
    assert [] == entity.data


def test_data_yaml_parse_error(tmpdir):
    file_path = tmpdir.join('entity.yml')
    file_path.write('what: nonsensical content: yes')
    entity = PlaybookOrTasklistFactory(str(file_path))
    assert [] == entity.data


@pytest.mark.parametrize('content, expected', [
    (None, 'tasklist'),
    ([], 'tasklist'),
    ([{}], 'tasklist'),
    ([{'debug': {'msg': 'foobar'}}], 'tasklist'),
    ([{'hosts': ''}], 'playbook'),
    ([{'roles': []}], 'playbook'),
    ([{'pre_tasks': []}], 'playbook'),
    ([{'tasks': []}], 'playbook'),
    ([{'post_tasks': []}], 'playbook'),
])
def test_typestring(tmpdir, content, expected):
    file_path = tmpdir.join('entity.yml')
    file_path.write(yaml.dump(content))

    entity = PlaybookOrTasklistFactory(str(file_path))

    assert expected == entity.typestring


def test_build_playbook_success(mocker, tmpdir):
    file = 'entity.yml'
    file_path = tmpdir.join(file)
    file_path.write(yaml.dump([{'hosts': ''}]))

    mock_pb_build = mocker.patch('ansiblediscover.entity.playbook.Playbook.build')
    mock_pb_build.return_value = Playbook([], str(file_path))

    PlaybookOrTasklistFactory(str(file_path)).build()
    mock_pb_build.assert_called_with(str(file_path))


def test_build_playbook_failure(mocker, tmpdir):
    file = 'entity.yml'
    file_path = tmpdir.join(file)
    file_path.write('what: nonsensical content: yes')

    mock_pb_build = mocker.patch('ansiblediscover.entity.playbook.Playbook.build')
    mock_pb_build.side_effect = RuntimeError()

    assert PlaybookOrTasklistFactory(str(file_path)).build() is None
    # Disabled; see `Playbook#build` why.
    # mock_pb_build.assert_called_with(str(file_path))


def test_build_failure():
    assert PlaybookOrTasklistFactory('does_not_exist').build() is None
