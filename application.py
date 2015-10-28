from flask import Flask
from flask import render_template
from jinja2 import Template
import tweet
import twiitit
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', tweets=twiitit.twiits(), 
testimuuttuja='testi2')
@app.route('/twitter')
def twitter():
    return 'Twitter is here'

@app.route('/about')
def about():
    return 'The about page'

if __name__ == '__main__':
    app.run(debug=True)
