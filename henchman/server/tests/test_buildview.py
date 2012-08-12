from nose.tools import raises
from ..tests import FlaskTest


class TestBuildView(FlaskTest):
    def test_index_action(self):
        req = self.app.get('/builds/')
        assert 'BuildViews index' in req.data

    def test_show_action(self):
        req = self.app.get('/builds/1a2b3c4')
        assert 'BuildViews show id:1a2b3c4' in req.data

    def test_post_action(self):
        req = self.app.post('/builds/', data={}, follow_redirects=True)
        assert 'BuildViews post' in req.data

    def test_delete_action(self):
        req = self.app.delete('/builds/1a2b3c4', follow_redirects=True)
        assert 'BuildViews delete id:1a2b3c4' in req.data

    @raises(NotImplementedError)
    def test_put_action(self):
        self.app.put('/builds/1a2b3c4', follow_redirects=True)

