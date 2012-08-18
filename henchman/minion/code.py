from henchman.settings import settings
from subprocess import Popen, PIPE
from os import path


class GitCommandNotFound(Exception):
    pass


class GitCommandError(Exception):
    pass


class Response(object):
    """
    """

    def __init__(self, proc, stdout=None, stderr=None):
        self.proc = proc
        self._stdout = stdout
        self._stderr = stderr

    @property
    def returncode(self):
        return self.proc.returncode.rstrip()

    @property
    def stdout(self):
        if self._stdout is None:
            return self.proc.stdout.rstrip()
        return self._stdout.rstrip()

    @property
    def stderr(self):
        if self._stderr is None:
            return self.proc.stderr.rstrip()
        return self._stderr.rstrip()


class Code(object):
    """
    """

    def __init__(self, build):
        self._stdout = ''
        self._stderr = ''
        self.build = build

    def update(self):
        """
        Update the code to be built. Either clone anew or reset to ref
        """
        self.git_binary = self._which_git()
        if self.git_binary:
            if self._repo_exists_for_build():
                self._fetch()
                self._reset()
            else:
                self._clone()
                self._reset()

    def _which_git(self):
        """
        Make sure that git is available
        `which` returns a 0 status code if the command was found, 1 if not
        """
        cmd = "which git"
        response = self._command(cmd)

        if response.proc.returncode == 0:
            return response.stdout
        raise GitCommandNotFound(response.stderr)

    def _fetch(self):
        """
        git fetch
        """
        print 'Code._fetch()'
        cmd = "cd %s && %s fetch" % (self.build.cwd, self.git_binary)
        return self._check_command_response(self._command(cmd))

    def _clone(self):
        """
        git clone repo path
        git reset --hard refspec
        """
        print 'Code._clone()'
        cmd = "%s clone %s %s" % (self.git_binary, self.build.repo_url,
            self.build.cwd)
        return self._check_command_response(self._command(cmd))

    def _reset(self):
        """
        git reset --hard refspec
        """
        print 'Code._reset()'
        cmd = "cd %s && %s reset --hard %s" % (self.build.cwd, self.git_binary,
            self.build.refspec)
        return self._check_command_response(self._command(cmd))

    def _repo_exists_for_build(self):
        """
        Check if there is a cloned repo for the build. Pretty primitive. :P
        """
        if path.exists(path.join(self.build.cwd, '.git')):
            return True
        return False

    def _command(self, command):
        """
        Execute given command and return the process object
        """
        print 'Code._command(): %s' % command
        proc = Popen(command, shell=True, stdout=PIPE, stdin=PIPE)
        stdout, stderr = proc.communicate(None)
        return Response(proc, stdout, stderr)

    def _check_command_response(self, response):
        if response.proc.returncode != 0:
            raise GitCommandError(response.stderr)
        return response
