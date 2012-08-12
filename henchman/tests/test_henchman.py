from henchman import Henchman
from nose.tools import assert_equal, raises


class TestHenchman(object):

    def test_create_minion_for_build(self):
        build_data = {
            'repo_url': 'git@github.com:plasticine/henchman.git',
            'steps': ['foo', 'bar']
        }
        henchman = Henchman()
        henchman.create_minion_for_build(build_data)
