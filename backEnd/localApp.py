from flask import Flask, render_template, request, redirect, url_for, make_response
##from dotenv import dotenv_values

import pymongo
import datetime
from bson.objectid import ObjectId
import sys

# instantiate the app
app = Flask(__name__)

# load credentials and configuration options from .env file
# if you do not yet have a file named .env, make one based on the template in env.example
config = dotenv_values(".env")

# turn on debugging if in development mode
if config['FLASK_ENV'] == 'development':
    # turn on debugging, if in development
    app.debug = True # debug mnode


# connect to the database
cxn = pymongo.MongoClient(config['MONGO_URI'], serverSelectionTimeoutMS=5000)
try:
    # verify the connection works by pinging the database
    cxn.admin.command('ping') # The ping command is cheap and does not require auth.
    db = cxn[config['promise_app']] # store a reference to the database
    print(' *', 'Connected to MongoDB!') # if we get here, the connection worked!
except Exception as e:
    # the ping command failed, so the connection is not available.
    # render_template('error.html', error=e) # render the edit template
    print(' *', "Failed to connect to MongoDB at", config['MONGO_URI'])
    print('Database connection error:', e) # debug


@app.route('/')
def show_home():
    response = make_response("Let's get started on making your promises!", 200)
    response.mimetype = "text/plain"
    return response

@app.route('/home-list-view')
def show_home_list_view():
    docs = db.promise_app.find({}).sort("date", -1)
    return render_template('frontEnd/homePageList.html', docs=docs)

@app.route('/create-promise')
def show_create_promise():
    return render_template('front-end/createPromise.html')

@app.route('/edit-promise')
def show_edit_promise():
    return render_template('front-end/editPromise.html')


@app.errorhandler(Exception)
def handle_error(e):
    """
    Output any errors - good for debugging.
    """
    return render_template('error.html', error=e) # render the edit template
