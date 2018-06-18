from flask import Flask, Response, request, render_template, redirect, url_for, session
from flaskext.mysql import MySQL
import datetime, os, shutil
from bson import Binary
from bson.objectid import ObjectId
from pymongo import MongoClient

app = Flask(__name__, static_folder="C:\\Users\\vaibh\\Desktop\\haxor\\dpApp\\static")

BASE = "C:\\Users\\vaibh\\Desktop\\haxor\\dpApp\\static\\uploads"
client = MongoClient()
client = MongoClient('localhost', 27017)

db = client['pymongo_test']

UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
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

        return render_template('index.html', data=tempData)




@app.route('/login/register', methods = ['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    if request.method == 'POST':
        values=["name","dob","ssn","mother","pno","email",'emailPass',"add","fwdadd","hardinq","empat","annsal","lenemp","emppno","empemail"]
        insVal= dict()
        for i in values:
            if request.form[i] =='':
                insVal[i] = "No Data Added"
            else:
                print(request.form[i])
                insVal[i] = request.form[i]
        cursor = posts.find({})
        lstUser = ()

        for i in cursor:
            lstUser = (i['_id'])
        print("Last value is {}".format(str(lstUser)))
        directory = "static/" + str(lstUser) +"/"


        if request.files['ssc']:

            directory = BASE + "\\" + str(lstUser) + "\\ssc\\"
            path1 = directory

            os.chmod(BASE, 0o777)
            print(os.path.exists(directory))
            if not os.path.exists(directory):
                os.makedirs(directory)
            request.files['ssc'].save(os.path.join(path1, request.files['ssc'].filename))
            insVal['ssc'] = path1 + request.files['ssc'].filename


        if request.files['dl']:

            directory = BASE + "\\" + str(lstUser) + "\\dl\\"
            path1 = directory

            os.chmod(BASE, 0o777)
            print(os.path.exists(directory))
            if not os.path.exists(directory):
                os.makedirs(directory)
            request.files['dl'].save(os.path.join(path1, request.files['dl'].filename))
            insVal['dl'] = path1 + request.files['dl'].filename

        if request.files['ub']:

            directory = BASE + "\\" + str(lstUser) + "\\ub\\"
            path1 = directory

            os.chmod(BASE, 0o777)
            print(os.path.exists(directory))
            if not os.path.exists(directory):
                os.makedirs(directory)
            request.files['ub'].save(os.path.join(path1, request.files['ub'].filename))
            insVal['ub'] = path1 + request.files['ub'].filename

        if request.files['ps']:

            directory = BASE + "\\" + str(lstUser) + "\\ps\\"
            path1 = directory

            os.chmod(BASE, 0o777)
            print(os.path.exists(directory))
            if not os.path.exists(directory):
                os.makedirs(directory)
            request.files['ps'].save(os.path.join(path1, request.files['ps'].filename))
            insVal['ps'] = path1+request.files['ps'].filename

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
        print(request.files['ssc'])
        return render_template('index.html', data=tempData)


@app.route('/userInfo/<id>', methods=['POST', 'GET'])
def userInfo(id):
    print(id)
    print("-----------------")
    cursor = posts.find({'_id': ObjectId(id)})
    temp = dict()
    for i in cursor:
        temp = i
    tList = []
    for k,v in temp.items():
        if k == '_id':
            continue
        else:
            tList.append((k,v))
    return render_template('userInformation.html', info = tList, user_id=id)


@app.route('/attachment/<id><type>', methods=['POST', 'GET'])
def attachment(id,type):
    print(id)
    print(type)
    binInfo=""
    search = posts.find({'_id':ObjectId(id)})
    for i in search:
        if type == '1':
            binInfo = i['ssc']
        elif type == '2':
            binInfo = i['dl']
        elif type == '3':
            binInfo = i['ub']
        elif type == '4':
            binInfo = i['ps']


    for i in search:
        print(i)
    print(binInfo)

    return render_template('attachments.html', user_id=binInfo)


if __name__ == '__main__':
    app.run()