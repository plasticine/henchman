from subprocess import Popen, PIPE

PENDING = None
PASSED = 'passed'
FAILED = 'failed'


class Step(object):
    """
    Steps represent single component commands in a build.
    """
    def __init__(self, cwd, command):
        self.cwd         = u"%s" % cwd
        self.command     = u"%s" % command
        self.cwd_command = u"cd %s; %s;" % (cwd, command)
        self.returncode  = PENDING

    @property
    def state(self):
        if self.returncode == None:
            return PENDING
        elif self.returncode == 0:
            return PASSED
        elif self.returncode != 0 or self.returncode > 0:
            return FAILED

    def execute(self):
        print 'Step.execute(): %s' % self.cwd_command
        self._process = Popen(
            self.cwd_command,
            shell   = True,
            stdout  = PIPE,
            stdin   = PIPE
        )
        self._stdout, self._stderr = self._process.communicate(None)
        self.returncode = self._process.returncode
