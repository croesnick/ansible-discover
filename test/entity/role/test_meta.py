import os

import pytest

from ansiblediscover.entity.role.meta import Meta


@pytest.mark.parametrize('content, expected_dependencies', [
    (None, []),
    ({}, []),
    ({'foobar': None}, []),
    ({'foobar': ['something']}, []),
    ({'dependencies': None}, []),
    ({'dependencies': {}}, []),
    ({'dependencies': []}, []),
    ({'dependencies': [{'role': 'dependency1'}]}, ['dependency1']),
    ({'dependencies': ['dependency1']}, ['dependency1']),
    ({'dependencies': ['dependency1', {'role': 'dependency2'}]}, ['dependency1', 'dependency2']),
    ({'dependencies': ['dependency1', 'dependency1']}, ['dependency1']),
    ({'dependencies': [{'role': 'dependency1'}, {'role': 'dependency1'}]}, ['dependency1']),
    ({'dependencies': [{'role': 'dependency1', 'attribute': 'foo'}]}, ['dependency1']),
])
def test_dependencies(content, expected_dependencies):
    meta = Meta(content, 'irrelevant_path')
    assert expected_dependencies == meta.dependencies()


def test_path_main():
    role_path = os.path.join('path', 'to', 'my', 'role')
    assert os.path.join(role_path, 'meta', 'main.yml') == Meta.path_main(role_path)
