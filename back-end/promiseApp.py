from flask import Flask, render_template, request, redirect, url_for, make_response
from dotenv import dotenv_values

import pymongo
import calendar
import datetime
from bson.objectid import ObjectId
import sys
import os

# instantiate the app
app = Flask(__name__, template_folder='../front-end',
            static_folder='../front-end/static')

# load credentials and configuration options from .env file
# if you do not yet have a file named .env, make one based on the template in env.example
config = dotenv_values(".env")

# turn on debugging if in development mode
if config['FLASK_ENV'] == 'development':
    # turn on debugging, if in development
    app.debug = True  # debug mnode


# connect to the database

# Database Schema
# DB Name: team13db
# Collection Name: promises
# data structure: {'"_id": "UUID (Auto-Generated)", "content": " ", "date": "%Y-%m-%d", "status": "completed / incomplete / ongoing"}

cxn = pymongo.MongoClient(config['MONGO_URI'], serverSelectionTimeoutMS=5000)
try:
    # verify the connection works by pinging the database
    # The ping command is cheap and does not require auth.
    cxn.admin.command('ping')
    db = cxn[config['MONGO_DBNAME']]  # store a reference to the database
    # if we get here, the connection worked!
    print(' *', 'Connected to MongoDB!')
except Exception as e:
    # the ping command failed, so the connection is not available.
    # render_template('error.html', error=e) # render the edit template
    print(' *', "Failed to connect to MongoDB at", config['MONGO_URI'])
    print('Database connection error:', e)  # debug


@app.route('/')
def show_home():
    response = make_response("Let's get started on making your promises!", 200)
    response.mimetype = "text/plain"
    return response


@app.route('/home-list-view')
def show_home_list_view():
    docs = db.promises.find({}).sort("date", -1)
    return render_template('homePageList.html', docs=docs)


@app.route('/home-calendar-view')
def show_home_calendar_view():
    request_year = request.args.get('year')
    request_month = request.args.get('month')

    today_date = datetime.date.today()

    if request_year and request_month and not (int(request_year) == today_date.year and int(request_month) == today_date.month):
        request_year = int(request_year)
        request_month = int(request_month)

        today_date = datetime.date(request_year, request_month, 1)
        today = {
            "year": request_year,
            "month": request_month,
            "day": 1,
            "month_eng": today_date.strftime("%B")
        }

        days_in_month = calendar.monthrange(request_year, request_month)[1]
        month_start_weekday = datetime.date(
            request_year, request_month, 1).weekday()
        month_end_weekday = datetime.date(
            request_year, request_month, days_in_month).weekday()
    else:
        today_date = datetime.date.today()
        today = {
            "year": today_date.year,
            "month": today_date.month,
            "day": today_date.day,
            "month_eng": today_date.strftime("%B")
        }

        days_in_month = calendar.monthrange(
            today_date.year, today_date.month)[1]
        month_start_weekday = datetime.date(
            today_date.year, today_date.month, 1).weekday()
        month_end_weekday = datetime.date(
            today_date.year, today_date.month, days_in_month).weekday()

    display_days = []
    display_prev_days = []
    display_next_days = []

    for i in range(month_start_weekday):
        display_prev_days.append({
            "cell_class": "month-prev",
            "current": 0
        })

    for day in range(1, days_in_month + 1):
        find_date = datetime.date(today_date.year, today_date.month, day)

        month_promises = db.promises.find_one({
            "date": f"{find_date.strftime('%Y')}-{find_date.strftime('%m')}-{find_date.strftime('%d')}"
        })

        if month_promises:
            if month_promises["status"] == "completed":
                display_days.append({
                    "day": day,
                    "cell_class": "completed",
                    "current": 1
                })
            elif month_promises["status"] == "incomplete":
                display_days.append({
                    "day": day,
                    "cell_class": "not-completed",
                    "current": 1
                })
            else:
                if find_date == datetime.date.today():
                    display_days.append({
                        "day": day,
                        "cell_class": "question",
                        "current": 1,
                        "today": 1,
                        "id": month_promises["_id"]
                    })
                else:
                    display_days.append({
                        "day": day,
                        "cell_class": "not-completed",
                        "current": 1
                    })
        else:
            if find_date == datetime.date.today():
                display_days.append({
                    "day": day,
                    "cell_class": "add",
                    "current": 1,
                    "today": 1
                })
            else:
                display_days.append({
                    "day": day,
                    "cell_class": "month-current",
                    "current": 1
                })

    for i in range(6 - month_end_weekday):
        display_next_days.append({
            "cell_class": "month-next",
            "current": 0
        })

    display_days = display_prev_days + display_days + display_next_days

    prev_month = datetime.date(
        today['year'], today['month'], 1) - datetime.timedelta(days=1)
    prev_month = {
        "year": prev_month.year,
        "month": prev_month.month
    }

    next_month = datetime.date(
        today['year'], today['month'], days_in_month) + datetime.timedelta(days=1)
    next_month = {
        "year": next_month.year,
        "month": next_month.month
    }

    return render_template('calendarView.html', today=today, display_days=display_days, prev_month=prev_month, next_month=next_month)


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


@app.route('/edit-promise', methods=['GET', 'POST'])
def show_edit_promise():

    if request.method == 'POST':
        if "delete" in request.form:
            idToDelete = request.form['delete']
            db.promises.delete_one({
                "_id": ObjectId(idToDelete)
            })
            #print('Hello world!', file=sys.stderr)
        else:
            idToEdit = request.form['editId']
            editContent = request.form['edit']
            #print(idToEdit, file=sys.stderr)
            db.promises.update_one({"_id": ObjectId(idToEdit)}, {
                                   "$set": {"content": editContent}})

    doc = {
        "content": "I will study for my physics exam.",
        "date": "2022-11-28",
        "status": "incomplete"
    }

    #mongoid = db.promises.insert_one(doc)
    data = db.promises.find({
            "date": {
             "$gte": "1900-1-1",
            }
    }).sort("date", -1)
    #print(data, file=sys.stderr)
    return render_template('editPromise.html', data=data)


@app.route('/search-promise', methods=['GET','POST'])
def show_search_promise():
    searchTag=""
    if request.method == 'POST':
        searchTag=request.form['search']
        #db.promises.drop_index('your field_text')
        db.promises.create_index([('content', 'text')])
        data=db.promises.find({
          "$text": {"$search": searchTag}
        }).sort("date", 1)
    else:
        data=db.promises.find({
        "date": {
             "$gte": "1900-1-1",
            }
        }).sort("date", -1)
    print(searchTag, file=sys.stderr)
    return render_template('searchPromise.html',data=data,searchTag=searchTag)


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
        # need to use query string to send a specific id for if-completed
        id = request.args.get('id')
        return render_template('ifCompleted.html', redirect_url=redirect_url, id=id)


# run the app
if __name__ == "__main__":
    #import logging
    # logging.basicConfig(filename='/home/ak8257/error.log',level=logging.DEBUG)
    app.run(debug=True)


@app.errorhandler(Exception)
def handle_error(e):
    """
    Output any errors - good for debugging.
    """
    return render_template('error.html', error=e)  # render the edit template
