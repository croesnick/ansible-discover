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
    else:
        tmpdir.ensure(path, file=True)
    with pytest.raises(ValueError):
        Entities.from_path(os.path.join(tmpdir, path), curdir=tmpdir)
