from flask import Flask, render_template, request, redirect
import mysql.connector
from db.api.req import *
from flask_login import LoginManager
from UserLogin import UserLogin
from FDataBase import FDataBase

# @login_manager.user_loader
# def load_user(user_id):
#     print("load_user")
#     return UserLogin().fromDB(user_id, db)


app = Flask(__name__)
db = mysql.connector.connect(
    host="localhost",
    user="Admin",
    password="Admin",
    database="algo",
)
db = FDataBase(db)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/auth', methods=['POST', 'GET'])
def auth():
    if request.method == 'GET':
        return render_template('authorization.html')
    elif request.method == 'POST':

        login, password = request.form['login'], request.form['passwd']

        return redirect('/')


@app.route('/registration', methods=['POST', 'GET'])
def registration():
    if request.method == 'GET':
        return render_template('registration.html')
    elif request.method == 'POST':
        username, login, password = request.form['name'], request.form['login'], request.form['passwd']
        photo = request.files['file']
        db.add_user(username, login, password, photo)
        return redirect('/')


@app.route('/account')
def account():
    return render_template('account.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
