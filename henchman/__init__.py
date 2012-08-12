from .queue.queue import Queue
from .minion.minion import Minion


class Henchman(object):
    """docstring for Henchman"""
    def __init__(self,):
        self.queue = Queue()

    def add_build(self, build_data):
        self.queue = self.queue.append(Minion(build_data))
