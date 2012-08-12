import hashlib
from os import path
from voluptuous import Schema, required, all, length, optional
from .step import Step
from henchman.settings import settings


class Build(object):
    """

    """

    _build_schema = Schema({
        required('repo_url'): all(str),
        required('steps'): all(list, length(min=1)),
        optional('refspec'): all(str)
    })

    def __init__(self, build_data):
        self._steps = None
        self._validate_build_data(build_data)
        self.build_data = build_data

    def _wrap_build_steps(self):
        return [Step(self.cwd, c) for c in self.build_data['steps']]

    def _validate_build_data(self, build_data):
        self._build_schema(build_data)

    @property
    def uuid(self):
        uuid = "%s:%s:%s" % (self.repo_url, self.refspec, '-'.join(self.build_data['steps']))
        return hashlib.sha224(uuid).hexdigest()[:7]

    @property
    def steps(self):
        if self._steps is None:
            self._steps = self._wrap_build_steps()
        return self._steps

    @property
    def cwd(self):
        return path.join(settings.build_root, self.uuid)

    @property
    def refspec(self):
        return "origin/%s" % self.build_data.get('refspec', 'master')

    @property
    def repo_url(self):
        return self.build_data['repo_url']
