from flask import Flask, render_template
import multiprocessing
import streaminstagram
import time, sys
import instaposts, twiitit, hashtags_twitter

"""

https://api.instagram.com/v1/subscriptions?client_secret
=bdadba8a4b274b45bdfcb306cfd6b120&client_id=efe6cccbd3ac4e75b842c957e954c569

curl -X DELETE 'https://api.instagram.com/v1/subscriptions?client_secret=bdadba8a4b274b45bdfcb306cfd6b120&object=all&client_id=efe6cccbd3ac4e75b842c957e954c569'

curl -F 'client_id=efe6cccbd3ac4e75b842c957e954c569' \
     -F 'client_secret=bdadba8a4b274b45bdfcb306cfd6b120' \
     -F 'object=tag' \
     -F 'aspect=media' \
     -F 'object_id=swag' \
     -F 'callback_url=https://nzmpqlpmhe.localtunnel.me/realtime' \
     https://api.instagram.com/v1/subscriptions/


lt --port 8000 --subdomain nzmpqlpmhe

"""

app = Flask(__name__)
app.add_url_rule('/realtime', methods = ['GET', 'POST'], view_func=streaminstagram.callback)


@app.route('/')
def index():
    return render_template('index.html', tweets=twiitit.twiits(), 
    	insta=instaposts.instagramPosts())
@app.route('/twitter')
def twitter():
    return 'Twitter is here'
@app.route('/about')
def about():
    return 'The about page'    

@app.route('/hashtags',methods = ['POST'])
def hashtags():
    return hashtags_twitter.tagit_twitter() 
    
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
#   instagramSubscription = multiprocessing.Process(target=initializeInstagram)
#   instagramSubscription.start()
   
   while True:
      try:
        time.sleep(1)
      except KeyboardInterrupt, SystemExit:
        instagramSubscription.terminate()
        flaskapp.terminate()
        sys.exit(0)