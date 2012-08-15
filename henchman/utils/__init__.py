import os
import sys


def ensure_exists(*paths):
    path = os.path.abspath(os.path.join(*paths))
    if not os.path.exists(path):
        os.makedirs(path)
    return path


def here(*paths):
    return os.path.join(os.path.dirname(sys._getframe(1).f_code.co_filename), *paths)
    # return os.path.abspath(os.path.join(os.path.dirname(__file__), *paths))
