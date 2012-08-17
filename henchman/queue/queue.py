from ..minion.minion import Minion, RUNNING


class Queue(object):
    """
    An instance of Queue represents
    """

    def __init__(self, queue=tuple()):
        self._queue = tuple(queue)

    def __len__(self):
        return len(self._queue)

    def __getitem__(self, key):
        return self._queue[key]

    @property
    def idle(self):
        return len(filter(lambda x: x.state == RUNNING, self._queue)) == 0

    def append(self, build):
        """
        Add an item to the internal queue and return a new Queue
        """
        return Queue(list(self._queue) + [build])

    def next(self):
        """
        Get the next build in the queue and return a new Queue instance
        as a tuple
        """
        return (list(self._queue).pop(0), Queue(self._queue[1:]))
