from .utils.logs import log
from .queue.queue import Queue
from .minion.minion import Minion
from .settings import settings


class Henchman(object):
    """docstring for Henchman"""

    __shared_state = {}

    def __init__(self):
        self.__dict__ = self.__shared_state
        self._queue = Queue()

    def create_minion_for_build(self, build_data):
        minion = Minion(build_data)
        self._queue = self._queue.append(minion)
        return minion
