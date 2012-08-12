from os import path, makedirs, rmdir
from tempfile import mkdtemp
from nose.tools import assert_equal, raises
from mock import Mock
from henchman.settings import Settings
from ..code import Code, GitCommandNotFound, GitCommandError
from ..build import Build


class TestCode(object):
    def setup(self):
        self.build_fixture = {
            'steps': ['foo', 'bar'],
            'refspec': 'master',
            'repo_url': 'git@github.com:plasticine/henchman.git'
        }
        self.build = Build(self.build_fixture)

    def _delete_build_cwd(self, build):
        if path.exists(build.cwd):
            rmdir(build.cwd)

    @raises(GitCommandNotFound)
    def test_which_git(self):
        """
        Check that we react properly if the `git` command is not available
        """
        code = Code(self.build)
        code._which_git = Mock(return_value=False)
        code.update()

    @raises(GitCommandError)
    def test_failed_git_command(self):
        """
        Check that we catch any git errors that arise from calling _clone or _reset
        """
        code = Code(self.build)

        response_mock = Mock()
        response_mock.status_code = 1
        response_mock.std_err = "HERP DERP!"

        code._clone = Mock(return_value=response_mock)
        code._reset = Mock(return_value=response_mock)
        code.update()

    def test_update_reset(self):
        """
        Test that if the code path already exits then update is run.
        """
        code = Code(self.build)
        code._clone = Mock()
        code._reset = Mock()
        code._check_response_status = Mock()

        self._delete_build_cwd(self.build)
        makedirs(self.build.cwd)
        code.update()

        code._reset.assert_called_once_with()
        assert not code._clone.called

    def test_update_clone(self):
        """
        If the code path does not exist then we need to do a full clone
        """
        code = Code(self.build)
        code._clone = Mock()
        code._reset = Mock()
        code._check_response_status = Mock()

        self._delete_build_cwd(self.build)

        code.update()

        code._clone.assert_called_once_with()
        code._reset.assert_called_once_with()
