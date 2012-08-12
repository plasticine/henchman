from ..tests import FlaskTest
import os
import tempfile
from nose.exc import SkipTest


class TestBuildView(FlaskTest):
    def test_index_action(self):
        req = self.app.get('/builds/')
        assert 'BuildViews index' in req.data

    def test_show_action(self):
        req = self.app.get('/builds/1')
        assert 'BuildViews show id:1' in req.data

    def test_post_action(self):
        req = self.app.post('/builds/')
        assert 'BuildViews post' in req.data

    def test_delete_action(self):
        req = self.app.delete('/builds/1')
        assert 'BuildViews delete id:1' in req.data

    def test_put_action(self):
        req = self.app.put('/builds/1')
        assert 'BuildViews put id:1' in req.data

