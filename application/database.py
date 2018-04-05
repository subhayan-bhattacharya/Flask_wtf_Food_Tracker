import sqlite3
from flask import g
import os
import sys

def connect_db():
    SITE_ROOT = os.path.dirname(os.path.realpath(os.path.dirname(__file__)))
    db_path = os.path.join(SITE_ROOT,'application\Food_Tracker.db')
    if os.path.exists(db_path):
        sql = sqlite3.connect(db_path)
    else:
        print "Could not find db file for loading"
        sys.exit()
    sql.row_factory = sqlite3.Row
    return sql

def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db