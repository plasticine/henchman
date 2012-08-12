import hashlib
from .step import Step


class Build(object):
    """

    """
    def __init__(self, build):
        self.build = build
        self.steps = self._wrap_build_steps()

    def _wrap_build_steps(self):
        return [Step(self.cwd, c) for c in self.build['steps']]

    @property
    def uuid(self):
        uuid = "%s:%s:%s" % (self.build['project'], self.refspec, self.build['id'])
        return hashlib.sha224(uuid).hexdigest()[:7]

    @property
    def cwd(self):
        return self.build['cwd']

    @property
    def refspec(self):
        return "origin/%s" % self.build['refspec']

    @property
    def remote_repo_url(self):
        return self.build['repo_url']
