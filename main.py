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
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'
login_manager = LoginManager(app)
db = mysql.connector.connect(
    host="localhost",
    user="Admin",
    password="Admin",
)
db = FDataBase(db)

@login_manager.user_loader
def load_user(user_id):
    print("load_user")
    return UserLogin().fromDB(user_id, db)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


@app.route('/')
def index():
    if current_user.is_authenticated:
        return render_template("index.html")
    return redirect('/auth')


@app.route('/auth', methods=['POST', 'GET'])
def auth():
    if request.method == 'GET':
        return render_template('authorization.html')
    elif request.method == 'POST':

        login, password = request.form['login'], request.form['passwd']
        user = db.getUserByLogin(login)
        print(user)
        if user and user[0][6] == password:
            userlogin = UserLogin().create(user)
            login_user(userlogin)
            return redirect('/')
        return redirect('/auth')


@app.route('/registration', methods=['POST', 'GET'])
def registration():
    if request.method == 'GET':
        return render_template('registration.html')
    elif request.method == 'POST':
        name, surname, thirdname = request.form['name'], request.form['surname'], request.form['thirdname']
        documentID = request.form['documentID']
        login, password = request.form['login'], request.form['passwd']
        photo = request.files['file']
        db.add_user(name, surname, thirdname, documentID, login, password, photo)
        return redirect('/')


@app.route('/account')
def account():
    data = current_user.getUserData()
    print(data)
    return render_template('account.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
