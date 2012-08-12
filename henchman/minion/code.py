from henchman.settings import Settings
from os import path
import envoy


class GitCommandNotFound(Exception):
    pass


class GitCommandError(Exception):
    pass


class Code(object):
    """

    """

    def __init__(self, build):
        self.build = build

    @property
    def _repo_clone_root(self):
        return path.join(Settings().build_root, self.build.uuid)

    def _check_response_status(self, response):
        if response.status_code != 0:
            raise GitCommandError(response.std_err)

    def _which_git(self):
        """
        Make sure that git is available
        `which` returns a 0 status code if the command was found, 1 if not
        """
        return not envoy.run("which git").status_code

    def _clone(self):
        """
        git clone repo path
        git reset --hard refspec
        """
        return envoy.run("git clone %s %s" % (self.remote_repo_url, self.build.cwd))

    def _reset(self):
        """
        git reset --hard refspec
        """
        return envoy.run("cd %s && git reset --hard %s" % (self._repo_clone_root, self.build.refspec))

    def update(self):
        if self._which_git():
            if path.exists(self._repo_clone_root):
                self._check_response_status(self._reset())
            else:
                self._check_response_status(self._clone())
                self._check_response_status(self._reset())
            return
        else:
            raise GitCommandNotFound
