from step import Step


class Build(object):
    """docstring for Build"""
    def __init__(self, build):
        self.build = build
        self.steps = self.wrap_build_steps()

    def wrap_build_steps(self):
        return [Step(step) for step in self.build['steps']]
