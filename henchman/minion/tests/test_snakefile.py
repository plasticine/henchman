from nose.tools import assert_equal, assert_not_equal, raises
from nose.exc import SkipTest
from henchman.utils import here
from ..snakefile.snakefile import Snakefile
from ..snakefile.task import Task
from ..snakefile.exceptions import SnakeFileMissingError, SnakeFileValidationError, SnakeFileYamlError, SnakeFileTaskUndefined


class TestSnakefile(object):
    def test_basic_parse(self):
        snakefile = Snakefile(path=here('fixtures', 'basic_snakefile.yml'))
        snakefile.parse()

        assert_equal(len(snakefile.tasks), 1)
        assert_equal(type(snakefile.task()), Task)
        assert_equal(snakefile.default, snakefile.task())
        assert_equal(snakefile.task().pre_build, None)
        assert_equal(snakefile.task().post_build, None)
        assert_equal(len(snakefile.task().steps), 1)
        assert_equal(snakefile.task().steps[0], "echo 'foo'")

    def test_multi_step_snakefile(self):
        snakefile = Snakefile(path=here('fixtures', 'multi_step_snakefile.yml'))
        snakefile.parse()

        assert_equal(len(snakefile.tasks), 1)
        assert_equal(type(snakefile.task()), Task)
        assert_equal(len(snakefile.task().steps), 3)
        assert_equal(snakefile.task().steps[0], "echo '1'")
        assert_equal(snakefile.task().steps[1], "echo '2'")
        assert_equal(snakefile.task().steps[2], "echo '3'")

    def test_multi_task_snakefile(self):
        snakefile = Snakefile(path=here('fixtures', 'multi_task_snakefile.yml'))
        snakefile.parse()

        assert_equal(len(snakefile.tasks), 3)
        assert_equal(snakefile.default, snakefile.task())
        assert_equal(snakefile.task(0).name, "I am the first task")
        assert_equal(snakefile.task(1).name, "I am the second task")
        assert_equal(snakefile.task(2).name, "I am the third task")

    def test_get_task_by_id(self):
        snakefile = Snakefile(path=here('fixtures', 'multi_task_snakefile.yml'))
        snakefile.parse()

        assert_equal(snakefile.task(1), snakefile.task(task_id="hamburger"))

    @raises(SnakeFileTaskUndefined)
    def test_get_invalid_task_by_id(self):
        snakefile = Snakefile(path=here('fixtures', 'multi_task_snakefile.yml'))
        snakefile.parse()

        snakefile.task(task_id="wat")

    @raises(SnakeFileValidationError)
    def test_invalid(self):
        Snakefile(path=here('fixtures', 'invalid_snakefile.yml')).parse()

    @raises(SnakeFileYamlError)
    def test_yaml_error(self):
        Snakefile(path=here('fixtures', 'malformed_snakefile.yml')).parse()

    @raises(SnakeFileMissingError)
    def test_missing(self):
        Snakefile(path=here('fixtures', 'i_am_not_here.yml')).parse()
