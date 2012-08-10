from buildqueue import BuildQueue
from nose.tools import assert_equal
from nose.tools import assert_not_equal


class TestBuildQueue(object):
    def test_immutable(self):
        """
        BuildQueue instances are immutable, if we modify them we get a
        new object back
        """
        build_queue = BuildQueue()
        new_build_queue = build_queue.append('foo')

        assert_equal(len(build_queue), 0)
        assert_equal(len(new_build_queue), 1)
        assert_not_equal(build_queue, new_build_queue)

    def test_append(self):
        build_queue = BuildQueue()
        new_build_queue = build_queue.append('foo')

        assert_equal(len(new_build_queue), 1)
        assert_equal(new_build_queue[0], 'foo')

    def test_multiple_append(self):
        build_queue = BuildQueue().append('foo').append('bar').append('ram')
        assert_equal(build_queue._queue, ('foo', 'bar', 'ram'))

    def test_next(self):
        build_queue = BuildQueue().append('foo').append('bar').append('ram')
        build, new_build_queue = build_queue.next()

        assert_equal(build, 'foo')
        assert_equal(len(build_queue), 3)
        assert_equal(len(new_build_queue), 2)
        assert_not_equal(build_queue, new_build_queue)
