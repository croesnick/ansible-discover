import os

import pytest

from ansiblediscover.entity import EntityFactoryABC


class EntityFactoryDummy(EntityFactoryABC):
    def __init__(self, path, name=None, typestring='dummy'):
        self._path = path
        self._name = os.path.basename(self._path) if name is None else name
        self._typestring = typestring

    @property
    def name(self):
        return self._name

    @property
    def path(self):
        return self._path

    @property
    def typestring(self):
        return self._typestring

    def build(self):
        pass


def test_key():
    file = 'tasks.yml'
    path = os.path.join('path', 'to', 'my', file)
    dummy = EntityFactoryDummy(path)
    assert ('dummy', file, path) == dummy.__key__()


def test_str():
    file = 'tasks.yml'
    path = os.path.join('path', 'to', 'my', file)
    dummy = EntityFactoryDummy(path)
    assert str(('dummy', file, path)) == str(dummy)


def test_eq_equals():
    d1 = EntityFactoryDummy(os.path.join('path', 'to', 'file.yml'))
    d2 = EntityFactoryDummy(os.path.join('path', 'to', 'file.yml'))

    assert d1 == d2


@pytest.mark.parametrize('lhs, rhs', [
    (EntityFactoryDummy(os.path.join('path', 'file.yml')),
     EntityFactoryDummy(os.path.join('path', 'file.yml'), name='file1.yml')),
    (EntityFactoryDummy(os.path.join('path', 'file.yml')),
     EntityFactoryDummy(os.path.join('path', 'file.yml'), typestring='foobar')),
    (EntityFactoryDummy('path1', name='file.yml'),
     EntityFactoryDummy('path2', name='file.yml')),
])
def test_eq_equals(lhs, rhs):
    assert lhs != rhs
