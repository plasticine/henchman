from gevent import Greenlet
from .build import Build
from .code import Code
from os import path
from .snakefile.snakefile import Snakefile

PENDING  = 0
RUNNING  = 1
FINISHED = 2


class Minion(Greenlet):
    """
    Minons are wrapper objects around a build and manage the starting,
    stopping and overall execution of each build.

    - Clone the git repo to local filesystem
    - Read Snakefile
    - Start Running build
    - Finish running build
    - Clean up git repo?
    - Save necessary things to DB.
    """
    def __init__(self, build_data):
        Greenlet.__init__(self)
        self.state     = PENDING
        self.build     = Build(build_data)
        self.code      = Code(self.build)
        self.snakefile = Snakefile(path.join(self.build.cwd, 'snakefile.yml'))

    def _run(self):
        self._state = RUNNING
        self.code.update()
        self.snakefile.parse()
        self._run_build_steps()
        self._cleanup()

    def _run_build_steps(self):
        pass

    def _cleanup(self):
        self._state = FINISHED
