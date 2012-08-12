from henchman.settings import settings
from henchman.server import app
from henchman import Henchman
from ..utils import mount
from .builds import BuildViews
from flask import render_template

henchman = Henchman()

@app.route('/')
def index():
    return render_template('index.html', henchman=henchman, settings=settings)


mount(app, BuildViews, 'builds', '/builds/', pk='build_uuid', pk_type='regex("[a-z0-9]{7}")')
