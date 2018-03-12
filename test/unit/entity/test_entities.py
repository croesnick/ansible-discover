import os

import pytest

from ansiblediscover.entity.entities import Entities


@pytest.mark.parametrize('path, expectation', [
    ('sample.yml', ('playbook', 'sample')),
    ('./sample.yml', ('playbook', 'sample')),
    ('roles/sample', ('role', 'sample')),
    ('./roles/sample', ('role', 'sample')),
    ('roles/sample/', ('role', 'sample')),
    ('./roles/sample/', ('role', 'sample')),
])
def test_from_path_success(tmpdir, path, expectation):
    tmpdir.ensure(path, file=True)
    assert expectation == Entities.from_path(os.path.join(tmpdir, path), curdir=tmpdir)


@pytest.mark.parametrize('path', [
    '',
    'sample',
    'subdir/sample.yml',
    'unroles/sample',
    'unroles/sample',
    'subdir/roles/sample',
])
def test_from_path_failure(tmpdir, path):
    if len(path.strip()) == 0:
        tmpdir.ensure(path, dir=True)
        full_path = path
    else:
        tmpdir.ensure(path, file=True)
        full_path = os.path.join(tmpdir, path)

    with pytest.raises(ValueError):
        Entities.from_path(full_path, curdir=tmpdir)


@pytest.mark.parametrize('playbooks, roles, expected_playbooks, expected_roles', [
    ({}, {}, [], []),
    ({'pb.yml': True}, {}, ['pb'], []),
    ({'pb.yml': False}, {}, [], []),
    ({}, {'roles/myrole': True}, [], ['myrole']),
    ({}, {'roles/myrole': False}, [], []),
    ({'pb.yml': True}, {'roles/myrole': True}, ['pb'], ['myrole']),
])
def test_from_paths(mocker, playbooks, roles, expected_playbooks, expected_roles):
    all_paths = {**playbooks, **roles}

    _original_from_path = getattr(Entities, 'from_path')

    def _mocked_from_path(path: str) -> str:
        if path not in all_paths:
            raise KeyError()

        if all_paths[path]:
            return _original_from_path(path)
        else:
            raise ValueError()

    mock_from_path = mocker.patch('ansiblediscover.entity.entities.Entities.from_path', wraps=_mocked_from_path)

    entities = Entities.from_paths(all_paths.keys())

    assert sorted(expected_playbooks) == sorted(entities['playbook'])
    assert sorted(expected_roles) == sorted(entities['role'])

    for path in all_paths:
        mock_from_path.assert_any_call(path)
