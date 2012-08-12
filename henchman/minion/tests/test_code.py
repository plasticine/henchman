from os import path, makedirs, rmdir
from tempfile import mkdtemp
from nose.exc import SkipTest
from nose.tools import assert_equal
from mock import patch
from henchman.settings import Settings
from ..code import Code
from ..build import Build


class TestCode(object):
    def setup(self):
        self.build_fixture = {
            'id': 1,
            'project': 'Test_project',
            'cwd': mkdtemp(),
            'steps': ['foo', 'bar'],
            'refspec': 'master',
            'repo_url': 'git@github.com:plasticine/henchman.git'
        }
        self.build = Build(self.build_fixture)

    def test_repo_clone_root(self):
        code = Code(self.build)
        assert_equal(code._repo_clone_root, path.join(Settings().build_root, self.build.uuid))

    @patch.object(Code, '_clone')
    @patch.object(Code, '_reset')
    def test_update_reset(self, mock_clone, mock_reset):
        """
        Test that if the code path already exits then update is run.
        """

        code = Code(self.build)
        rmdir(code._repo_clone_root)
        makedirs(code._repo_clone_root)
        code.update()

        mock_reset.assert_called_once_with()
        assert not mock_clone.called

    @patch.object(Code, '_clone')
    @patch.object(Code, '_reset')
    def test_update_clone(self, mock_clone, mock_reset):
        """
        If the code path does not exist then we need to do a full clone
        """
        code = Code(self.build)
