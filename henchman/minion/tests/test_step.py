from ..step import Step, WAITING, PASSED, FAILED
from nose.tools import assert_equal
from tempfile import mkdtemp


class TestStep(object):
    def __init__(self):
        self.temp_dir = mkdtemp()

    def test_state(self):
        step = Step(cwd=self.temp_dir, command="ls")

        # the default returncode state is None
        assert_equal(step.state, WAITING)

        step.returncode = 0
        assert_equal(step.state, PASSED)

        step.returncode = 1
        assert_equal(step.state, FAILED)

    def test_execute(self):
        step = Step(cwd=self.temp_dir, command="echo 'ROFLCOPTER'")
        step.execute()

        assert_equal(step.returncode, 0)
        assert_equal(step._stdout, "ROFLCOPTER\n")

        step = Step(cwd=self.temp_dir, command="pwd")
        step.execute()

        assert_equal(step._stdout, self.temp_dir + "\n")
