import stat

import pytest
from ruamel import yaml

from ansiblediscover.utils.fs import FS


def test_load_yaml_raises_on_invalid_yaml(tmpdir):
    content = 'this: is: invalid'

    task_file = tmpdir.join("mydata.yml")
    task_file.write(content)

    with pytest.raises(TypeError):
        FS.load_yaml(str(task_file))


def test_load_yaml_raises_on_missing_file(tmpdir):
    task_file = tmpdir.join('mydata.yml')

    with pytest.raises(OSError):
        FS.load_yaml(str(task_file))


def test_load_yaml_raises_on_wrong_file_permissions(tmpdir):
    task_file = tmpdir.join("mydata.yml")
    task_file.write('irrelevant')
    task_file.chmod(stat.S_IWUSR)

    with pytest.raises(OSError):
        FS.load_yaml(str(task_file))


def test_load_yaml_succeeds_on_valid_yaml(tmpdir):
    content = ['hello', {'this': 'is valid yaml'}]

    task_file = tmpdir.join("mydata.yml")
    task_file.write(yaml.dump(content))

    assert content == FS.load_yaml(str(task_file))