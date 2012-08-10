class BuildQueue(object):
    """
    An instance of Buildqueue represents
    """

    def __init__(self, queue=tuple()):
        self._queue = tuple(queue)

    def __len__(self):
        return len(self._queue)

    def __getitem__(self, key):
        return self._queue[key]

    def append(self, build):
        """
        Add an item to the internal queue and return a new BuildQueue
        """
        return BuildQueue(list(self._queue) + [build])

    def next(self):
        """
        Get the next build in the queue and return a new BuildQueue instance
        as a tuple
        """
        return (list(self._queue).pop(0), BuildQueue(self._queue[1:]))
