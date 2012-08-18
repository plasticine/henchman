import gevent
from .utils.logs import log
from .queue.queue import Queue
from .minion.minion import Minion
from .settings import settings


class Henchman(object):
    """docstring for Henchman"""

    __shared_state = {}
    __monitor = None

    def __init__(self):
        self.__dict__ = self.__shared_state
        self._run()

    def create_minion_for_build(self, build_data):
        minion = Minion(build_data)
        self._queue = self._queue.append(minion)
        return minion

    def _run(self):
        if self.__monitor is None:
            self.log = log
            self._queue = Queue()
            self.__monitor = gevent.spawn(self._monitor_queue)

    def _monitor_queue(self):
        while True:
            if self._queue.idle and len(self._queue) > 0:
                minion, queue = self._queue.next()
                self._queue = queue
                minion.start()
            gevent.sleep(settings.queue.poll_interval)
