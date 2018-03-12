from ansiblediscover.entity.tasklist import TasklistFactory


def test_init():
    path = 'path/to/my/tasks.yml'
    assert path == TasklistFactory(path).path


def test_name():
    tasklist = TasklistFactory('path/to/my/tasks.yml')
    assert 'tasks.yml' == tasklist.name


def test_typestring():
    assert 'tasklist' == TasklistFactory('irrelevant').typestring


def test_build():
    assert TasklistFactory('irrelevant').build() is None
