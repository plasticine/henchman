from subprocess import Popen, PIPE

WAITING = None
PASSED = 'passed'
FAILED = 'failed'


class Step(object):
    """
    Steps represent single component commands in a build.
    """
    def __init__(self, command):
        self.command     = command
        self.stdin_pipe  = PIPE
        self.stdout_pipe = PIPE
        self.returncode  = WAITING

    @property
    def state(self):
        if self.returncode == None:
            return WAITING
        elif self.returncode == 0:
            return PASSED
        elif self.returncode != 0 or self.returncode > 0:
            return FAILED

    def execute(self):
        self._process = Popen(
            self.command,
            cwd     = self.cwd,
            shell   = True,
            stdout  = self.stdin_pipe,
            stdin   = self.stdout_pipe
        )
        self._stdout, self._stderr = self._process.communicate(None)
        self.returncode = self._process.returncode
