from flask import Flask, render_template, request, redirect, abort, url_for, make_response

app = Flask(__name__)

@app.route('/')
def show_home():
    response = make_response("Let's get started on making your promises!", 200)
    response.mimetype = "text/plain"
    return response

@app.route('/home-list-view')
def show_home_list_view():
    return render_template('frontEnd/homePageList.html')

@app.route('/create-promise')
def show_create_promise():
    return render_template('frontEnd/createPromise.html')

@app.route('/edit-promise')
def show_edit_promise():
    return render_template('frontEnd/editPromise.html')


