from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/auth', methods=['POST', 'GET'])
def auth():
    if request.method == 'GET':
        return render_template('authorization.html')
    elif request.method == 'POST':
        username, login, password = request.form['name'], request.form['login'], request.form['passwd']
        file = request.files['file']
        file.save(f"static/img/{file.filename}")
        print(username, login, password, file)


@app.route('/register')
def register():
    return render_template('registration.html')


if __name__ == '__main__':
    app.run()
