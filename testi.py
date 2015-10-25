from flask import Flask
from flask import render_template
from jinja2 import Template
import tweet
import sqlite3 as sql3
import time
import json
app = Flask(__name__)

con = sql3.connect("tweets.db")
a = []
cur = con.execute("SELECT username, tweet FROM taula")
for row in cur:
	a.append( [ row[0], row[1]] )

print a;
con.close()

@app.route('/')
def index():
    return render_template('feed.html', tweets=a)
    
if __name__ == '__main__':
    app.run(debug=True)