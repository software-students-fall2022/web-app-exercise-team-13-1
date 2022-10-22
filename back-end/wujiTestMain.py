from flask import Flask, render_template, request, redirect, url_for, make_response
from dotenv import dotenv_values
from wujiTestFunction import *

import pymongo
import datetime
from bson.objectid import ObjectId
import sys

temp=1;
wuji();
# instantiate the app
app = Flask(__name__, template_folder="../front-end",static_folder='../front-end/static')

# load credentials and configuration options from .env file
# if you do not yet have a file named .env, make one based on the template in env.example
config = dotenv_values("wuji.env")

# turn on debugging if in development mode
if config['FLASK_ENV'] == 'development':
    # turn on debugging, if in development
    app.debug = True # debug mnode


# connect to the database
cxn = pymongo.MongoClient(config['MONGO_URI'], serverSelectionTimeoutMS=5000)
try:
    # verify the connection works by pinging the database
    cxn.admin.command('ping') # The ping command is cheap and does not require auth.
    db = cxn[config['MONGO_DBNAME']] # store a reference to the database
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
    return render_template('homePageList.html')

@app.route('/create-promise')
def show_create_promise():
    return render_template('createPromise.html')

@app.route('/search-promise', methods=['GET','POST'])
def show_search_promise():
    searchTag=""
    if request.method == 'POST':
        searchTag=request.form['search']
    #db.wc1629.drop_index('your field_text')
    db.wc1629.create_index([('content', 'text')])
    data=db.wc1629.find({
      "$text": {"$search": searchTag}
    })
    print(searchTag, file=sys.stderr)
    return render_template('searchPromise.html',data=data)

@app.route('/edit-promise', methods=['GET','POST'])
def show_edit_promise():
    
    if request.method == 'POST':
        if "delete" in request.form:
             idToDelete=request.form['delete']
             db.wc1629.delete_one({
                "_id": ObjectId(idToDelete)
              })
             #print('Hello world!', file=sys.stderr)
        else:
             idToEdit=request.form['editId']
             editContent=request.form['edit']
             #print(idToEdit, file=sys.stderr)
             db.wc1629.update_one({"_id": ObjectId(idToEdit)},{"$set": {"content":editContent}})
            
    doc = {
        "content": "I will study for my physics exam.",
        "date": "2022-11-28",
        "status": "incomplete"
    }
    
    #mongoid = db.wc1629.insert_one(doc)
    data=db.wc1629.find({
        "date": {
             "$gte": "2022-11-1",
             "$lte": "2022-11-31"
            }
    }).sort("date", -1)
    #print(data, file=sys.stderr)
    return render_template('editPromise.html',data=data)


