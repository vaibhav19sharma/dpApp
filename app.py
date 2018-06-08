from flask import Flask, Response, request, render_template, redirect, url_for, session
from flaskext.mysql import MySQL
import datetime, os, shutil

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('homescreen.html')


@app.route('/login/', methods=['POST', 'GET'])
def login():
    username = request.form['username']
    password = request.form['pass']
    if(username == "admin" and password == "admin"):
        return render_template('index.html', data="Invalid Credentials")


@app.route('/login/register')
def register():
    return render_template('register.html')


if __name__ == '__main__':
    app.run()