from henchman import Henchman
from nose.tools import assert_equal, assert_not_equal, raises


class TestHenchman(object):

    def test_create_minion_for_build(self):
        build_data = {
            'repo_url': ['git@github.com:plasticine/henchman.git'],
            'steps': ['foo', 'bar']
        }
        henchman = Henchman()
        queue = henchman._queue
        henchman.create_minion_for_build(build_data)
        assert_not_equal(queue, henchman._queue)
