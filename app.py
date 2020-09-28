from flask import Flask, render_template, request
from flask_cors import CORS
from models import create_post, get_posts
import main
import os

app = Flask(__name__)

CORS(app)

@app.route('/', methods = ['GET', 'POST'])
def index():

    if request.method == 'GET':
        pass

    if request.method == 'POST':
        name = request.form.get('name')
        post = request.form.get('post')
        #create_post(name, post)

    posts  = get_posts()

    return render_template('index.html', posts=posts)

@app.route('/play/')
def play():
   return main.main([15,10])

@app.route('/play_hard/')
def play_hard():
   return main.main([25,20])

@app.route('/play_easy/')
def play_easy():
   return main.main([15,8])
    
if __name__ == "__main__":
    app.run(debug=True)