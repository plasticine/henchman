from ..build import Build
from ..step import Step
from nose.exc import SkipTest
from nose.tools import assert_equal
from nose.tools import assert_not_equal


class TestBuild(object):

    def test_wrap_build_steps(self):
        build = Build({'steps': ['foo', 'bar']})

        wrapped_steps = build.wrap_build_steps()
        assert_equal(len(wrapped_steps), 2)
        assert isinstance(wrapped_steps[0], Step)
        assert isinstance(wrapped_steps[1], Step)
