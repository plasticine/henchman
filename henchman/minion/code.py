from henchman.settings import Settings
from os import path
from pbs import git


class Code(object):
    """

    """

    def __init__(self, build):
        self.build = build

    @property
    def _repo_clone_root(self):
        return path.join(Settings().build_root, self.build.uuid)

    def _clone(self):
        """
        git clone repo path
        git reset --hard refspec
        """
        git.clone(self.build.remote_repo_url, self.build.cwd)

    def _reset(self):
        """
        git reset --hard refspec
        """
        git.reset(self.build.refspec, hard=True)

    def update(self):
        if path.exists(self._repo_clone_root):
            self._reset()
        else:
            self._clone()
            self._reset()
        return
