#!/usr/bin/env python

from gevent import monkey; monkey.patch_all()
from henchman.server import app

if __name__ == '__main__':
    app.run(debug=True)
