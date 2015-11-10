from flask import Flask
import multiprocessing
import streaminstagram
import time, sys

"""
https://api.instagram.com/v1/subscriptions?client_secret
=bdadba8a4b274b45bdfcb306cfd6b120&client_id=efe6cccbd3ac4e75b842c957e954c569
"""

app = Flask(__name__)
app.add_url_rule('/realtime', methods = ['GET', 'POST'], view_func=streaminstagram.callback)


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
    
class ApplicationProcess(multiprocessing.Process):

    def __init__(self, ):
        multiprocessing.Process.__init__(self)
        self.exit = multiprocessing.Event()

    def run(self):
        try:
            startApp()
        except (KeyboardInterrupt, SystemExit):
            print "Exiting..."

    def terminate(self):
        print "Flask application shutdown initiated"
        self.exit.set()
    
    
def startApp():
    global app
    app.run(debug=True, port=8000, use_reloader=True)


def initializeInstagram():
    streaminstagram.startSubscription()    
    
    
if __name__ == '__main__':
   flaskapp = ApplicationProcess()
   flaskapp.start()
   instagramSubscription = multiprocessing.Process(target=initializeInstagram)
   instagramSubscription.start()
   
   while True:
      try:
        time.sleep(1)
      except KeyboardInterrupt, SystemExit:
        instagramSubscription.terminate()
        flaskapp.terminate()
        sys.exit(0)