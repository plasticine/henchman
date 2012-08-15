

class Task(object):
    """

    """
    def __init__(self, task):
        self._task = task

    @property
    def name(self):
        return self._task['name']

    @property
    def id(self):
        return self._task.get('id', None)

    @property
    def pre_build(self):
        return self._task['build'].get('pre_build', None)

    @property
    def post_build(self):
        return self._task['build'].get('post_build', None)

    @property
    def steps(self):
        steps = self._task['build']['steps']
        if type(steps) == str:
            steps = [steps]
        return tuple(steps)

