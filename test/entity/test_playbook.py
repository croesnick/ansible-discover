import pytest
from ansiblediscover.entity.playbook import Playbook


def test_initialize_contents():
    contents = ['foo', 'bar']
    assert Playbook(contents).contents == contents


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
