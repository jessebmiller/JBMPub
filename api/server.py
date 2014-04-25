import sqlite3

from settings import *

conn = sqlite3.connect(DB)
cur = conn.cursor()
