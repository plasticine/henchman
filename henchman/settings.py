import yaml
from os import path
from .utils import here, ensure_exists
from .utils.memoize import memoized


class objectify(dict):
    def __init__(self, d):
        self.__dict__ = self
        map(self.__setitem__, d.keys(), d.values())


class Settings(object):
    """docstring for Settings"""

    __shared_state = {}

    def __init__(self):
        self.__dict__ = self.__shared_state
        self.settings = self._load(here('../settings.yml'))
        self.logs_root = ensure_exists(here('../../../logs'))
        self.tmp_root = ensure_exists(here('../../../tmp'))
        self.build_root = ensure_exists(path.join(self.tmp_root, 'builds'))

    def __getattr__(self, name):
        return objectify(self.settings[name])

    @memoized
    def _load(self, settings_file):
        return yaml.load(file(settings_file, 'r'))

settings = Settings()
