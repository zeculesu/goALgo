from flask import Flask, render_template, request, redirect
import mysql.connector
from db.api.req import *
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from UserLogin import UserLogin
from FDataBase import FDataBase
from time import time
from data import get_data, draw_graf
from datetime import datetime, timedelta


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


@app.route('/widgets')
@login_required
def widgets():
    data = datetime.now() - timedelta(days=1)
    data = data.strftime('%Y-%m-%d')
    yndx = get_data('YNDX', data, 0)[::-1][:15]
    sber = get_data('SBER', data, 0)[::-1][:15]
    vtb = get_data('VTBR', data, 0)[::-1][:15]
    rosn = get_data('ROSN', data, 0)[::-1][:15]
    gasp = get_data('GASP', data, 0)[::-1][:15]
    draw_graf('static/img/candle_yndx.png', yndx)
    draw_graf('static/img/candle_sber.png', sber)
    draw_graf('static/img/candle_vtb.png', vtb)
    draw_graf('static/img/candle_rosn.png', rosn)
    draw_graf('static/img/candle_gasp.png', gasp)

    return render_template('widgets.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
