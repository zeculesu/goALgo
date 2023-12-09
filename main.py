from flask import Flask, render_template, request, redirect
import mysql.connector
from db.api.req import *

app = Flask(__name__)
db = mysql.connector.connect(
    host="localhost",
    user="Admin",
    password="Admin",
    database="algo",
)
cursor = db.cursor()


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
        add_user(cursor, username, login, password, photo)
        db.commit()
        return redirect('/')


if __name__ == '__main__':
    app.run()
