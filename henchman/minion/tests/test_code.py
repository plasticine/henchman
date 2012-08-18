from os import path
from tempfile import mkdtemp
from nose.tools import assert_equal, raises
from nose.exc import SkipTest
from mock import Mock, patch
from henchman.settings import Settings
from ..code import Code, Response, GitCommandNotFound, GitCommandError
from ..build import Build


class TestCode(object):
    def setup(self):
        self.build_fixture = {
            'steps': ['foo', 'bar'],
            'refspec': 'master',
            'repo_url': ['git@github.com:plasticine/henchman.git']
        }
        self.build = Build(self.build_fixture)

    def test_which_git(self):
        """
        Ensure that we can locate the git binary. We should store the path to
        the git binary.
        """

        proc_mock = Mock()
        proc_mock.returncode = 0
        response = Response(proc_mock, '/usr/local/bin/git', '')
        code = Code(self.build)
        code._command = Mock(return_value=response)

        assert_equal(code._which_git(), '/usr/local/bin/git')

    @raises(GitCommandError)
    def test_failing_git_command(self):
        """
        Make sure we properly wrap up any failing git commands in an exception
        """
        code = Code(self.build)

        proc_mock = Mock()
        proc_mock.returncode = 1
        response = Response(proc_mock, '', 'herp derp')
        code._command = Mock(return_value=response)
        code._which_git = Mock(return_value='lol')
        code.update()

    @raises(GitCommandNotFound)
    def test_no_git_binary(self):
        """
        Make sure that we raise GitCommandNotFound if the git binary is
        not available.
        """
        code = Code(self.build)

        proc_mock = Mock()
        proc_mock.status_code = 1
        response = Response(proc_mock, '', 'herp derp')
        code._command = Mock(return_value=response)
        code.update()  # raises GitCommandNotFound

    def test_update_reset(self):
        """
        If the build cwd exists then we should run a reset on the repo
        """
        code = Code(self.build)
        code._clone = Mock()
        code._reset = Mock()
        code._repo_exists_for_build = Mock(return_value=True)

        code.update()

        code._reset.assert_called_once_with()
        assert not code._clone.called

    def test_update_clone_reset(self):
        """
        if the build cwd doesn't exist then the we need to clone and then reset
        """
        code = Code(self.build)
        code._clone = code._reset = Mock()
        code._reset = Mock()
        code._check_response_status = Mock()
        code._repo_exists_for_build = Mock(return_value=False)

        code.update()

        code._clone.assert_called_once_with()
        code._reset.assert_called_once_with()
