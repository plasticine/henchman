from henchman.server import app

class FlaskTest(object):
    def setup(self):
        app.config['TESTING'] = True
        self.app = app.test_client()
