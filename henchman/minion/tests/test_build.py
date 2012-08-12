from ..build import Build
from ..step import Step
from nose.exc import SkipTest
from nose.tools import assert_equal
from nose.tools import assert_not_equal
from tempfile import mkdtemp


class TestBuild(object):
    def __init__(self):
        self.temp_dir = mkdtemp()

    def test_wrap_build_steps(self):
        build = Build({
            'cwd': self.temp_dir,
            'steps': ['foo', 'bar']
        })

        wrapped_steps = build._wrap_build_steps()
        assert_equal(len(wrapped_steps), 2)
        assert isinstance(wrapped_steps[0], Step)
        assert isinstance(wrapped_steps[1], Step)
