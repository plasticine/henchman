from step import Step


class Build(object):
    """docstring for Build"""
    def __init__(self, build):
        self.build = build
        self.steps = self.wrap_build_steps()

    @property
    def cwd(self):
        return self.build['cwd']

    def wrap_build_steps(self):
        return [Step(self.cwd, c) for c in self.build['steps']]
