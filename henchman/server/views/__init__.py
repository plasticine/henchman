from henchman.settings import Settings
from henchman.server import app
from ..utils import mount
from .builds import BuildViews
from flask import render_template


@app.route('/')
def index():
    return render_template('index.html', settings=Settings())


mount(app, BuildViews, 'builds', '/builds/', pk='build_uuid', pk_type='regex("[a-z0-9]{7}")')
