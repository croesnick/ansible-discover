# import pytest
#
# from ansiblediscover.entity.factories.includes_list import IncludesList
#
#
# @pytest.mark.parametrize('content, expected_includes', [
#     ([], []),
#     ([{}], []),
#     ([{'debug': {'msg': 'foo'}}], []),
#     ([{'include': 'good.yml'}], ['include:task:good.yml']),
#     ([{'include': 'bad'}], []),
#     ([{'include_tasks': 'good.yml'}], ['include:task:good.yml']),
#     ([{'include_tasks': 'bad'}], []),
#     ([{'import_tasks': 'good.yml'}], ['include:task:good.yml']),
#     ([{'import_tasks': 'bad'}], []),
#     ([{'include_role': {'name': 'good'}}], ['include:role:good']),
#     ([{'include_role': 'bad'}], []),
#     ([{'import_role': {'name': 'good'}}], ['include:role:good']),
#     ([{'import_role': 'bad'}], []),
#     ([{'import_playbook': 'bad.yml'}], []),
#     ([{'block': [
#         {'include': 'good1.yml'},
#         {'include_tasks': 'good2.yml'},
#         {'debug': {'msg': 'foo'}},
#         {'import_tasks': 'good3.yml'},
#         {'include_role': {'name': 'good4'}},
#         {'import_role': {'name': 'good5'}}
#     ]}], ['include:task:good1.yml', 'include:task:good2.yml', 'include:task:good3.yml',
#           'include:role:good4', 'include:role:good5']),
# ])
# def test_build_succeeds(content, expected_includes):
#     includes = [include.identifier() for include in IncludesList.build(content).items()]
#     assert sorted(expected_includes) == sorted(includes)
