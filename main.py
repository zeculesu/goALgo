from flask import Flask, render_template, request, redirect
import mysql.connector
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from UserLogin import UserLogin
from FDataBase import FDataBase
from data import get_data, draw_graf, draw_graf_value, draw_graf_volume
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
db.delete_db()
db.make_db()


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
        if current_user.is_authenticated:
            return redirect('/account')
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
@login_required
def account():
    data = current_user.getUserData()[1:-1].replace("'", "").split(", ")
    return render_template('account.html', data=data)


@app.route('/widgets')
@login_required
def widgets():
    data = datetime.now() - timedelta(days=1)
    data = data.strftime('%Y-%m-%d')
    yndx = get_data('YNDX', data, 0)[::-1][:15][::-1]
    sber = get_data('SBER', data, 0)[::-1][:15][::-1]
    vtb = get_data('VTBR', data, 0)[::-1][:15][::-1]
    rosn = get_data('ROSN', data, 0)[::-1][:15][::-1]
    gasp = get_data('GASP', data, 0)[::-1][:15][::-1]
    for name, act in zip(["yndx", "sber", "vtb", "rosn", "gasp"], [yndx, sber, vtb, rosn, gasp]):
        draw_graf(f'static/img/candle_{name}.png', act)
        draw_graf_value(f'static/img/value_{name}.png', act)
        draw_graf_volume(f'static/img/volume_{name}.png', act)
    return render_template('widgets.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
