from ..build import Build, InvalidBuildPostData
from ..step import Step
from nose.exc import SkipTest
from nose.tools import assert_equal, assert_not_equal, raises
from tempfile import mkdtemp
from os import path
from henchman.settings import settings


class TestBuildSchema(object):
    @raises(InvalidBuildPostData)
    def test_build_data_missing_key_steps(self):
        Build({'repo_url': ['git@github.com:plasticine/henchman.git']})

    @raises(InvalidBuildPostData)
    def test_build_data_invalid_key_steps(self):
        Build({'repo_url': ['git@github.com:plasticine/henchman.git'], 'steps': []})

    @raises(InvalidBuildPostData)
    def test_build_data_invalid_key_steps2(self):
        Build({'repo_url': ['git@github.com:plasticine/henchman.git'], 'steps': 'test'})

    @raises(InvalidBuildPostData)
    def test_build_data_missing_key_repo_url(self):
        Build({'steps': ['herp']})

    @raises(InvalidBuildPostData)
    def test_build_data_missing_key_repo_url(self):
        Build({'steps': ['herp', 'derp']})

    @raises(InvalidBuildPostData)
    def test_build_data_invalid_optional_key_refspec(self):
        Build({'repo_url': ['git@github.com:plasticine/henchman.git'], 'steps': ['herp', 'derp'], 'refspec': ''})


class TestBuild(object):
    def __init__(self):
        self.temp_dir = mkdtemp()

    def test_wrap_build_steps(self):
        build = Build({'repo_url': ['git@github.com:plasticine/henchman.git'], 'steps': ['herp', 'derp']})

        wrapped_steps = build._wrap_build_steps()
        assert_equal(len(wrapped_steps), 2)
        assert isinstance(wrapped_steps[0], Step)
        assert isinstance(wrapped_steps[1], Step)

    def test_uuid(self):
        """
        Encoding differences in post data should not make for a differend uuid being generated.
        """
        unicode_build_data = Build({'repo_url': [u'git@github.com:plasticine/henchman.git'], 'steps': [u'herp', u'derp']})
        build_data = Build({'repo_url': ['git@github.com:plasticine/henchman.git'], 'steps': ['herp', 'derp']})

        assert_equal(unicode_build_data.uuid, build_data.uuid)

    def test_cwd(self):
        build = Build({'repo_url': ['git@github.com:plasticine/henchman.git'], 'steps': ['herp', 'derp']})

        assert_equal(build.cwd, path.join(settings.build_root, build.uuid))
