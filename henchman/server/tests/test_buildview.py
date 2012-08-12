from henchman import Henchman
from henchman.minion.minion import Minion
from nose.tools import raises, assert_equal
from ..tests import FlaskTest

henchman = Henchman()


class TestBuildView(FlaskTest):

    _build_post_data = {'repo_url': ['git@github.com:plasticine/henchman.git'], 'steps': ['herp', 'derp']}

    def test_index_action(self):
        req = self.app.get('/builds/')

        assert_equal(req.status_code, 200)
        assert 'BuildViews index' in req.data

    def test_show_action(self):
        req = self.app.get('/builds/1a2b3c4')

        assert_equal(req.status_code, 200)
        assert 'BuildViews show id:1a2b3c4' in req.data

    def test_valid_post_action(self):
        """
        You should be able to add new items to the build queue by posting
        data. Also test that the henchman._queue object gets bigger.
        """
        queue_length = len(henchman._queue)
        req = self.app.post('/builds/', data=self._build_post_data, follow_redirects=True)
        build_uuid = Minion(self._build_post_data).build.uuid

        assert_equal(req.status_code, 200)
        assert_equal(queue_length + 1, len(henchman._queue))
        assert 'BuildViews show id:%s' % (build_uuid) in req.data

    def test_invalid_post_action(self):
        """
        Invalid post requests should recieve a 400 status code
        """
        data = dict(self._build_post_data)
        data['steps'] = []
        req = self.app.post('/builds/', data=data, follow_redirects=True)

        assert_equal(req.status_code, 400)

    def test_delete_action(self):
        req = self.app.delete('/builds/1a2b3c4', follow_redirects=True)

        assert_equal(req.status_code, 200)
        assert 'BuildViews delete id:1a2b3c4' in req.data

    @raises(NotImplementedError)
    def test_put_action(self):
        self.app.put('/builds/1a2b3c4', follow_redirects=True)
