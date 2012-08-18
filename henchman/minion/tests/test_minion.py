from ..minion import Minion
from ..code import Code
from mock import Mock, patch
from nose.exc import SkipTest


class TestMinion(object):
    def setup(self):
        self.build_fixture = {
            'steps': ['foo', 'bar'],
            'refspec': 'master',
            'repo_url': ['git@github.com:plasticine/henchman.git']
        }

    @patch.object(Code, 'update')
    def test_lol(self, update_mock):
        minion = Minion(build_data=self.build_fixture)
        minion.code.update()

        raise SkipTest
