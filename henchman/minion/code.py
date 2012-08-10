from pbs import git


class Code(object):
    """docstring for Code"""
    def __init__(self, build):
        self.build = build

    def _clone(self):
        """
        git clone repo path
        git reset --hard refspec
        """
        git.clone(self.build.remote_url, self.cwd)

    def _reset(self):
        """
        git reset --hard refspec
        """
        git.reset(self.build.refspec, hard=True)
