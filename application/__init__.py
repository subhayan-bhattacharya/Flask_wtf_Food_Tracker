__package__ = "application"

from flask import Flask,g
from os import urandom

app = Flask(__name__,template_folder='templates')

app.config['DEBUG'] = True
app.config['SECRET_KEY'] = urandom(24)

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

from views import *

