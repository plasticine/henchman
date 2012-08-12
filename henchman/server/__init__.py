from flask import Flask
from .utils import RegexConverter

app = Flask(__name__)
app.config.from_object(__name__)
app.url_map.converters['regex'] = RegexConverter

import views
