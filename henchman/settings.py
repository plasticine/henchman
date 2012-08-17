import yaml
from .utils import here, ensure_exists
# yaml.load_all(snakefile_file)

class Settings(object):
    """docstring for Settings"""

    __shared_state = {}

    def __init__(self):
        self.__dict__ = self.__shared_state
        self.tmp_path = ensure_exists(here('../../../tmp'))
        self.logs_path = ensure_exists(here('../../../logs'))

    @property
    def tmp_root(self):
        return self.tmp_path

    @property
    def build_root(self):
        return ensure_exists(self.tmp_root, 'builds')

    @property
    def logs_root(self):
        return self.logs_path

settings = Settings()
