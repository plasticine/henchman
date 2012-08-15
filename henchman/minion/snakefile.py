from os import path
from voluptuous import Schema, InvalidList, required, all, length, optional
import yaml
from .task import Task


class SnakeFileMissingError(Exception):
    pass


class SnakeFileValidationError(Exception):
    pass


class SnakeFileYamlError(Exception):
    pass


class SnakeFileTaskUndefined(Exception):
    pass


class Snakefile(object):
    """
    Snakefiles are YAML files that describe how to build a project.
    """

    _snakefile_task_schema = Schema({
        optional('id'): all(str, length(min=1)),
        required('name'): all(str, length(6)),
        required('build'): {
            required('steps'): all(list, length(min=1)),
            optional('pre_build'): all(list, length(min=1)),
            optional('post_build'): all(list, length(min=1))
        }
    })

    def __init__(self, path):
        self.path = path

    @property
    def default(self):
        return self.task(0)

    def task(self, task=0, task_id=None):
        if task_id is not None:
            try:
                return filter(lambda x: x.id == task_id, self.tasks)[0]
            except IndexError, err:
                raise SnakeFileTaskUndefined(err)
        return self.tasks[task]

    def parse(self):
        self.tasks = self._validate(self._load())

    def _load(self):
        if path.exists(self.path):
            snakefile_file = file(self.path, 'r')
            try:
                snakefile_yaml = list(yaml.load_all(snakefile_file))
            except Exception, err:
                if hasattr(err, 'problem_mark'):
                    raise SnakeFileYamlError("line %s, col %s" % (err.problem_mark.line, err.problem_mark.column))
                raise SnakeFileYamlError(err)
            return snakefile_yaml
        raise SnakeFileMissingError()

    def _validate(self, snakefile_yaml):
        _tasks = []
        try:
            for task_yaml in snakefile_yaml:
                if task_yaml is not None:
                    task = Task(self._snakefile_task_schema(task_yaml))
                    _tasks.append(task)
        except InvalidList, err:
            raise SnakeFileValidationError(err)
        return _tasks
