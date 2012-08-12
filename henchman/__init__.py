from .queue.queue import Queue
from .minion.minion import Minion


class Henchman(object):
    """docstring for Henchman"""

    __shared_state = {}

    def __init__(self,):
        self.__dict__ = self.__shared_state
        self.queue = Queue()

    def add_build(self, build_data):
        self.queue = self.queue.append(Minion(build_data))
