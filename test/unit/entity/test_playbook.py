import pytest
import stat
from ruamel import yaml

from ansiblediscover.entity.playbook import Playbook


def test_build_success(tmpdir):
    content = [{'hosts': 'all', 'remote_user': 'root', 'roles': []}]

    playbook_file = tmpdir.join('playbook.yml')
    playbook_file.write(yaml.dump(content))

    assert content == Playbook.build(str(playbook_file)).content


def test_build_fails_on_invalid_yaml(tmpdir):
    content = 'certainly: not: yaml'

    playbook_file = tmpdir.join('playbook.yml')
    playbook_file.write(content)

    with pytest.raises(RuntimeError):
        Playbook.build(str(playbook_file))


def test_build_fails_on_nonreadable_yaml(tmpdir):
    content = [{'hosts': 'all'}]

    playbook_file = tmpdir.join('playbook.yml')
    playbook_file.write(yaml.dump(content))
    playbook_file.chmod(stat.S_IWUSR)

    with pytest.raises(RuntimeError):
        Playbook.build(str(playbook_file))


def test_initialize_contents():
    contents = ['foo', 'bar']
    assert Playbook(contents).content == contents


@pytest.mark.parametrize('contents, expected_roles', [
    ([], set()),
    ([{'roles': []}], set()),
    ([{'roles': ['good11']}], {'good11'}),
    ([{'roles': ['good11', 'good12']}], {'good11', 'good12'}),
    ([{'roles': [{'role': 'good21'}]}], {'good21'}),
    ([{'roles': [{'role': 'good21'}, {'role': 'good22'}]}], {'good21', 'good22'}),
    ([{'roles': [{'role': 'good21'}, 'good11']}], {'good11', 'good21'}),
    ([{'roles': [{'name': 'bad21'}]}], set()),
    ([{'roles': [[], {}]}], set()),
    ([{'roles': [{'name': 'bad21'}, 'good11']}], {'good11'}),
    ([{'roles': [{'name': 'bad21'}, {'role': 'good21'}]}], {'good21'}),
])
def test_extract_role_names(contents, expected_roles):
    model = Playbook(contents)
    assert model.roles_from_plays() == expected_roles
