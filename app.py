from flask import Flask, Response, request, render_template, redirect, url_for, session
from flaskext.mysql import MySQL
import datetime, os, shutil
from bson.objectid import ObjectId

from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient()
client = MongoClient('localhost', 27017)

db = client['pymongo_test']


posts = db.projectX
for i in posts.find({}):
    print(i['_id'])
temp = posts.find_one({'name': 'Vaibhav Sharma'})
@app.route('/')
def hello_world():
    return render_template('homescreen.html')


@app.route('/login/', methods=['POST', 'GET'])
def login():
    username = request.form['username']
    password = request.form['pass']
    if(username == "admin" and password == "admin"):
        tempData = []
        cursor = posts.find({})
        if cursor is not None:
            for i in cursor:
                tempData.append((i['name'],i['_id']))
        else:
            tempData = ["Add users"]
        print(tempData)
        return render_template('index.html', data=tempData)




@app.route('/login/register', methods = ['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    if request.method == 'POST':
        values=["name","dob","ssn","mother","pno","email","add","fwdadd","hardinq","ssc","dl","ub","ps","empat","annsal","lenemp","emppno","empemail"]
        insVal= dict()
        for i in values:
            print(i)
            if request.form[i] =='':
                insVal[i] = "No Data Added"
            else:
                print(request.form[i])
                insVal[i] = request.form[i]

        print(insVal)
        posts.insert(insVal)
        print("inserted successfully")
        tempData = []
        cursor = posts.find({})
        if cursor is not None:
            for i in cursor:
                tempData.append((i['name'],i['_id']))
        else:
            tempData = ["Add users"]
        print(tempData)
        return render_template('index.html', data=tempData)


@app.route('/userInfo/<id>', methods=['POST', 'GET'])
def userInfo(id):
    print("-----------------")
    cursor = posts.find({'_id': ObjectId(id)})
    temp = dict()
    for i in cursor:
        temp = i
    print(temp)
    tList = []
    for k,v in temp.items():
        if k == '_id':
            continue
        else:
            tList.append((k,v))

    print(tList)
    return render_template('userInformation.html', info = tList)
if __name__ == '__main__':
    app.run()