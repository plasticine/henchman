from ..queue import Queue
from henchman.minion.minion import PENDING, RUNNING, FINISHED
from nose.tools import assert_equal
from nose.tools import assert_not_equal
from mock import MagicMock


class TestQueue(object):
    def test_immutable(self):
        """
        BuildQueue instances are immutable, if we modify them we get a
        new object back
        """
        queue = Queue()
        new_queue = queue.append('foo')

        assert_equal(len(queue), 0)
        assert_equal(len(new_queue), 1)
        assert_not_equal(queue, new_queue)

    def test_queue_idle(self):
        queue = Queue()
        minion1 = MagicMock()
        minion2 = MagicMock()
        minion3 = MagicMock()
        minion1.state = PENDING
        minion2.state = PENDING
        minion3.state = PENDING

        queue._queue = (minion1, minion2, minion3,)
        assert_equal(queue.idle, True)

        minion2.state = FINISHED
        queue._queue = (minion1, minion2, minion3,)
        assert_equal(queue.idle, True)

        minion2.state = RUNNING
        queue._queue = (minion1, minion2, minion3,)
        assert_equal(queue.idle, False)


    def test_append(self):
        queue = Queue()
        new_queue = queue.append('foo')

        assert_equal(len(new_queue), 1)
        assert_equal(new_queue[0], 'foo')

    def test_multiple_append(self):
        queue = Queue().append('foo').append('bar').append('ram')
        assert_equal(queue ._queue, ('foo', 'bar', 'ram'))

    def test_next(self):
        queue = Queue().append('foo').append('bar').append('ram')
        build, new_queue = queue .next()

        assert_equal(build, 'foo')
        assert_equal(len(queue), 3)
        assert_equal(len(new_queue), 2)
        assert_not_equal(queue, new_queue)
