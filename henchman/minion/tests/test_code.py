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

        if path.exists(code._repo_clone_root):
            rmdir(code._repo_clone_root)
        makedirs(code._repo_clone_root)
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

        if path.exists(code._repo_clone_root):
            rmdir(code._repo_clone_root)

        code.update()

        code._clone.assert_called_once_with()
        code._reset.assert_called_once_with()
