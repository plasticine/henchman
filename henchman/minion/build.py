import hashlib
from os import path
from voluptuous import Schema, InvalidList, required, all, length, optional
from .step import Step
from henchman.settings import settings
from henchman.utils.memoize import memoized


class InvalidBuildPostData(Exception):
    pass


class Build(object):
    """

    """

    _build_schema = Schema({
        required('repo_url'): all(list, length(1)),
        required('steps'): all(list, length(min=1)),
        optional('refspec'): all(str, length(min=1))
    })

    def __init__(self, build_data):
        self._validate_build_data(build_data)
        self.build_data = build_data

    def _wrap_build_steps(self):
        return [Step(self.cwd, s) for s in self.build_data['steps']]

    def _validate_build_data(self, build_data):
        try:
            self._build_schema(build_data)
        except InvalidList, err:
            raise InvalidBuildPostData(err)

    @property
    @memoized
    def uuid(self):
        steps_id = u'-'.join([u"%s" % s for s in self.build_data['steps']])
        uuid = u"%s:%s:%s" % (self.repo_url, self.refspec, steps_id)
        return hashlib.sha224(uuid).hexdigest()[:7]

    @property
    @memoized
    def steps(self):
        return self._wrap_build_steps()

    @property
    def cwd(self):
        return u"%s" % path.join(settings.build_root, self.uuid)

    @property
    def refspec(self):
        return u"origin/%s" % self.build_data.get('refspec', 'master')

    @property
    def repo_url(self):
        return u"%s" % self.build_data['repo_url'][0]
