import stat

import pytest
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


def test_initialize_content():
    content = ['foo', 'bar']
    path = 'myplaybook.yml'

    assert content == Playbook(content, path).content
    assert path == Playbook(content, path).path
    assert 'myplaybook' == Playbook(content, path).name()


@pytest.mark.parametrize('content, expected_dependencies', [
    ([], []),
    ([{'roles': ['good11', {'role': 'good12'}]}], ['roles/good11', 'roles/good12']),
])
def test_dependencies(content, expected_dependencies):
    model = Playbook(content, 'irrelevant_path')
    assert expected_dependencies == sorted(d.path for d in model.dependencies())


@pytest.mark.parametrize('content, expected_dependencies', [
    ([], []),
    ([{'include': 'good.yml'}], ['good.yml']),
    ([{'include': 'bad'}], []),
    ([{'include': None}], []),
    ([{'include': []}], []),
    ([{'include': 'good.yml'}, {'roles': ['irrelevant']}], ['good.yml']),
    ([{'import_playbook': 'good.yml'}], ['good.yml']),
    ([{'import_playbook': 'bad'}], []),
    ([{'import_playbook': None}], []),
    ([{'import_playbook': []}], []),
    ([{'import_playbook': 'good.yml'}, {'roles': ['irrelevant']}], ['good.yml']),
])
def test_playbook_dependencies(content, expected_dependencies):
    model = Playbook(content, 'irrelevant_path')
    assert expected_dependencies == sorted(d.path for d in model.playbook_dependencies())


@pytest.mark.parametrize('content, expected_dependencies', [
    ([], set()),
    ([{'roles': []}], set()),
    ([{'roles': ['good11']}], {'roles/good11'}),
    ([{'roles': ['good11', 'good12']}], {'roles/good11', 'roles/good12'}),
    ([{'roles': [{'role': 'good21'}]}], {'roles/good21'}),
    ([{'roles': [{'role': 'good21'}, {'role': 'good22'}]}], {'roles/good21', 'roles/good22'}),
    ([{'roles': [{'role': 'good21'}, 'good11']}], {'roles/good11', 'roles/good21'}),
    ([{'roles': [{'name': 'bad21'}]}], set()),
    ([{'roles': [[], {}]}], set()),
    ([{'roles': [{'name': 'bad21'}, 'good11']}], {'roles/good11'}),
    ([{'roles': [{'name': 'bad21'}, {'role': 'good21'}]}], {'roles/good21'}),
    ([{'pre_tasks': []}], set()),
    ([{'pre_tasks': [{'debug': {'msg': 1}}]}], set()),
    ([{'tasks': []}], set()),
    ([{'tasks': [{'debug': {'msg': 1}}]}], set()),
    ([{'post_tasks': []}], set()),
    ([{'post_tasks': [{'debug': {'msg': 1}}]}], set()),
])
def test_play_dependencies(content, expected_dependencies):
    model = Playbook(content, 'irrelevant_path')
    assert expected_dependencies == {d.path for d in model.play_dependencies()}


def test_extract_name():
    assert 'myplaybook' == Playbook.extract_name('myplaybook.yml')
