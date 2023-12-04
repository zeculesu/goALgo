from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/auth')
def auth():
    return render_template('authorization.html')


@app.route('/register')
def register():
    return render_template('registration.html')


if __name__ == '__main__':
    app.run()
