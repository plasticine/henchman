from ..queue import Queue
from henchman.minion.minion import PENDING, RUNNING, FINISHED
from nose.tools import assert_equal
from nose.tools import assert_not_equal
from mock import MagicMock


class TestQueueState(object):
    def setup(self):
        self.queue = Queue()
        self.m1 = MagicMock()
        self.m2 = MagicMock()
        self.m3 = MagicMock()
        self.m1.state = PENDING
        self.m2.state = PENDING
        self.m3.state = PENDING

    def test_queue_empty(self):
        self.queue._queue = ()
        assert_equal(self.queue.idle, True)

    def test_queue_pending(self):
        self.queue._queue = (self.m1, self.m2, self.m3,)
        assert_equal(self.queue.idle, True)

    def test_queue_finished(self):
        self.m2.state = FINISHED
        self.queue._queue = (self.m1, self.m2, self.m3,)
        assert_equal(self.queue.idle, True)

    def test_queue_running(self):
        self.m2.state = RUNNING
        self.queue._queue = (self.m1, self.m2, self.m3,)
        assert_equal(self.queue.idle, False)


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
        assert_equal(len(queue), 3)

        b1, q1 = queue.next()
        assert_equal(b1, 'foo')
        assert_equal(len(q1), 2)
        assert_not_equal(queue, q1)

        b2, q2 = q1.next()
        assert_equal(b2, 'bar')
        assert_equal(len(q2), 1)
        assert_not_equal(q1, q2)

        b3, q3 = q2.next()
        assert_equal(b3, 'ram')
        assert_equal(len(q3), 0)
        assert_not_equal(q2, q3)
