import os


def ensure_exists(*paths):
    path = os.path.abspath(os.path.join(*paths))
    if not os.path.exists(path):
        os.makedirs(path)
    return path


def here(*paths):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), *paths))



class Settings(object):
    """docstring for Settings"""

    __shared_state = {}

    def __init__(self):
        self.__dict__ = self.__shared_state
        self.tmp_path = ensure_exists(here('../../../tmp'))

    @property
    def tmp_root(self):
        return ensure_exists(self.tmp_path)

    @property
    def build_root(self):
        return ensure_exists(self.tmp_root, 'builds')
