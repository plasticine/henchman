from step import Step, WAITING, PASSED, FAILED
from nose.tools import assert_equal
from nose.exc import SkipTest


class TestStep(object):
    def test_state(self):
        step = Step(command="ls")

        # the default returncode state is None
        assert_equal(step.state, WAITING)

        step.returncode = 0
        assert_equal(step.state, PASSED)

        step.returncode = 1
        assert_equal(step.state, FAILED)


class TestCode(object):
    raise SkipTest


class TestMinion(object):
    raise SkipTest
