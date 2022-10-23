from flask import Flask, render_template, request, redirect, url_for, make_response
from dotenv import dotenv_values

import pymongo
import datetime
from bson.objectid import ObjectId
import sys
import os

# instantiate the app
app = Flask(__name__, template_folder='../front-end', static_folder='../front-end/static')

# load credentials and configuration options from .env file
# if you do not yet have a file named .env, make one based on the template in env.example
config = dotenv_values(".env")

# turn on debugging if in development mode
if config['FLASK_ENV'] == 'development':
	# turn on debugging, if in development
	app.debug = True # debug mnode


# connect to the database

# Database Schema 
# DB Name: team13db
# Collection Name: promises
# data structure: {'"_id": "UUID (Auto-Generated)", "content": " ", "date": "%Y-%m-%d", "status": "completed / incomplete / ongoing"}

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

@app.route('/create-promise', methods=['GET', 'POST'])
def show_create_promise():
	if request.method == 'POST':
		# Create promise data from form
		create_promise = request.form['promise']
		redirect_url = request.form['redirect_url']

		create_data = {
			'content': create_promise,
			'date': datetime.datetime.now().strftime('%Y-%m-%d'),
			'status': 'ongoing',
		}
		
		db.promises.insert_one(create_data)

		# Redirect to other page
		return redirect(redirect_url)
	elif request.method == 'GET':
		redirect_url = request.args.get('redirect_url')
		return render_template('createPromise.html', redirect_url=redirect_url)


@app.route('/edit-promise')
def show_edit_promise():
	return render_template('editPromise.html')

@app.route('/if-completed', methods=['GET', 'POST'])
def show_if_completed():
	if request.method == 'POST':
		# Update promise data from form
		if_completed = request.form['if-completed']
		redirect_url = request.form['redirect_url']
		id = request.form['id']

		if_completed_mapper = {
			'Yes': 'completed',
			'No': 'incomplete'
		}

		update_data = {
			'status': if_completed_mapper[if_completed]
		}
		
		db.promises.update_one({"_id": ObjectId(id)}, {"$set": update_data})

		# Redirect to other page
		return redirect(redirect_url)
	elif request.method == 'GET':
		redirect_url = request.args.get('redirect_url')
		id = request.args.get('id') #need to use query string to send a specific id for if-completed
		return render_template('ifCompleted.html', redirect_url=redirect_url, id=id)
	




# run the app
if __name__ == "__main__":
	#import logging
	#logging.basicConfig(filename='/home/ak8257/error.log',level=logging.DEBUG)
	app.run(debug = True)


