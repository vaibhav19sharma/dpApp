from flask import Flask, Response, request, render_template, redirect, url_for, session
from flaskext.mysql import MySQL
import datetime, os, shutil

from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient()
client = MongoClient('localhost', 27017)

db = client['pymongo_test']


posts = db.posts
post_data = {
    'title': 'Python and MongoDB',
    'content': 'PyMongo is fun, you guys',
    'author': 'Scott'
}
result = posts.insert_one(post_data)
print('One post: {0}'.format(result.inserted_id))
bills_post = posts.find_one({'title': 'Python and MongoDB'})
print(bills_post)


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