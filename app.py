from flask import Flask, Response, request, render_template, redirect, url_for, session
from flaskext.mysql import MySQL
import datetime, os, shutil
from bson import Binary
from bson.objectid import ObjectId

import time
from itertools import chain
import email
import imaplib
from email.mime.text import MIMEText
import smtplib


from pymongo import MongoClient

app = Flask(__name__, static_folder = "static")

BASE = "static/"
client = MongoClient()
client = MongoClient('localhost', 27017)

db = client['pymongo_test']

UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
posts = db.demoOne
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
                tempData.append((i['Name'],i['_id']))
        else:
            tempData = ["Add users"]

        return render_template('index.html', data=tempData)




@app.route('/login/register', methods = ['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    if request.method == 'POST':
        values=["Name","Date_Of_Birth","Social_Security_Number","Mother","PhoneNumber","Email",'Emails_Password',"Address","Forwarded_Address","Hard_Inquiry","Employeed_At","Annual_Salary","Length_Employment","Employer_Phone_Number","Employer_Email","Number_Of_TradeLines","Number_Of_Cards_Applied_For","Number_Of_Cards"]
        insVal= dict()
        # import pdb
        # pdb.set_trace()
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

            directory = BASE + "/" + str(lstUser) + "/ssc/"
            path1 = directory

            os.chmod(BASE, 0o777)
            print(os.path.exists(directory))
            if not os.path.exists(directory):
                os.makedirs(directory)
            request.files['ssc'].save(os.path.join(path1, request.files['ssc'].filename))
            insVal['ssc'] = path1 + request.files['ssc'].filename


        if request.files['dl']:

            directory = BASE + "/" + str(lstUser) + "/dl/"
            path1 = directory

            os.chmod(BASE, 0o777)
            print(os.path.exists(directory))
            if not os.path.exists(directory):
                os.makedirs(directory)
            request.files['dl'].save(os.path.join(path1, request.files['dl'].filename))
            insVal['dl'] = path1 + request.files['dl'].filename

        if request.files['ub']:

            directory = BASE + "/" + str(lstUser) + "/ub/"
            path1 = directory

            os.chmod(BASE, 0o777)
            print(os.path.exists(directory))
            if not os.path.exists(directory):
                os.makedirs(directory)
            request.files['ub'].save(os.path.join(path1, request.files['ub'].filename))
            insVal['ub'] = path1 + request.files['ub'].filename

        if request.files['ps']:

            directory = BASE + "/" + str(lstUser) + "/ps/"
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
                tempData.append((i["Name"],i['_id']))
        else:
            tempData = ["Add users"]
        print(request.files['ssc'])


        return render_template('addCardandTrade.html', data=tempData[-1][1], numberTrade = int(insVal['Number_Of_TradeLines']), numberCardApplied= int(insVal['Number_Of_Cards_Applied_For']), numberCard = int(insVal['Number_Of_Cards']))

@app.route('/addCardandTrade/<id>', methods = ['POST','GET'])
def addCardandTrade(id):
    if request.method == 'GET':
        return render_template('addCardandTrade.html')
    if request.method == 'POST':

        tl_bankname = request.form.getlist('Bank_Name')
        tl_crLimit = request.form.getlist('Credit_Limit')
        tl_age= request.form.getlist('Age_Of_Account')
        tl_status=request.form.getlist('Status')
        tl_openclose=request.form.getlist('Tradeline_Open_Close')

        add_bankname=request.form.getlist('Bank_Name_Card')
        add_date=request.form.getlist('Date_Applied')
        add_applies=request.form.getlist('Card_Applies_For')
        add_status=request.form.getlist('Status_Card')

        active_bankname=request.form.getlist('ActiveBank_Name_Card')
        active_limit=request.form.getlist('Credit_Limit_Card')
        active_balance=request.form.getlist('Balance_Card')
        trade=[]
        tradeLine= dict()
        applied=[]
        app_cards= dict()
        active=[]
        active_cards = dict()

        for i in range(len(tl_bankname)):
            tradeLine['BankName']=tl_bankname[i]
            tradeLine['Credit_Limit']= tl_crLimit[i]
            tradeLine['Age']= tl_age[i]
            tradeLine['Status']=tl_status[i]
            tradeLine['Open_Close']=tl_openclose
            trade.append(tradeLine)

        for i in range(len(add_bankname)):
            #import pdb
            #pdb.set_trace()
            app_cards['BankName']=add_bankname[i]
            app_cards['Date_Apllied']=add_date[i]
            app_cards['Applies']=add_applies[i]
            app_cards['Status']=add_status[i]
            applied.append(app_cards)

        for i in range(len(active_bankname)):
            active_cards['BankName']= active_bankname[i]
            active_cards['Limit']= active_limit[i]
            active_cards['Balance']=active_balance[i]
            active.append(active_cards)
        id_new =id.replace("'","")

        tempData = []
        cursor = posts.find({'_id': ObjectId(id_new)})
        posts.update({'_id': ObjectId(id_new)},{
            "$set" : {"TradeLines":trade, "ActiveCards":active, "AppliedCards":applied}
        })
        if cursor is not None:
            for i in cursor:
                tempData.append((i["Name"],i['_id']))
        else:
            tempData = ["Add users"]
        print(posts.find({'_id':ObjectId(id_new)}))

        return render_template('index.html', data=tempData)

@app.route('/userInfo/<id>', methods=['POST', 'GET'])
def userInfo(id):
    print(id)
    user_id= id
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
    print("tList Print :",tList)

    print (tList[0][1],tList[5][1], tList[6][1])
    imap_ssl_host = 'imap.gmail.com'  # imap.mail.yahoo.com
    imap_ssl_port = 993
    username = tList[5][1]
    password =tList[6][1]
    
    # Restrict mail search. Be very specific.
    # Machine should be very selective to receive messages.
    criteria = {
        'FROM': '',
        'SUBJECT': '',
        'BODY': '',
}
    uid_max = 0
    server = imaplib.IMAP4_SSL(imap_ssl_host, imap_ssl_port)
    server.login(username, password)
    server.select('inbox')
    
    result, data = server.uid('search', None, 'ALL')
    #print(int.from_bytes(data[0], byteorder=''))
    uids = [int(s) for s in data[0].split()]
    
    if uids:
        uid_max = max(uids)
    # Initialize `uid_max`. Any UID less than or equal to `uid_max` will be ignored subsequently.

    server.logout()

# Keep checking messages ...
# I don't like using IDLE because Yahoo does not support it.

# Have to login/logout each time because that's the only way to get fresh results.

    server = imaplib.IMAP4_SSL(imap_ssl_host, imap_ssl_port)
    server.login(username, password)
    server.select('inbox')
    result, data = server.uid('search', None, 'ALL')

    uids = [int(s) for s in data[0].split()]

    all_mails = []
    i=0
    for uid in uids:
        # Have to check again because Gmail sometimes does not obey UID criterion.
        #if uid > uid_max:
        result, data = server.uid('fetch', str(uid), '(RFC822)')  # fetch entire message
        msg = email.message_from_string(str(data[0][1]))
        i=i+1
        uid_max = uid

            
        text = get_first_text_block(msg)
        print ('New message :::::::::::::::::::::')
        print (msg)
        all_mails.append(msg)
        if i>10:
            break

    server.logout()
    time.sleep(1)

    return render_template('userInformation.html', info=tList, msgs = all_mails, user_id = user_id)




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

    return render_template('attachments.html', user_id=binInfo[8:len(binInfo)])




def search_string(uid_max, criteria):
    c = list(map(lambda t: (t[0], '"' + str(t[1]) + '"'), criteria.items())) + [('UID', '%d:*' % (uid_max + 1))]
    return '(%s)' % ' '.join(chain(*c))
    # Produce search string in IMAP format:
    #   e.g. (FROM "me@gmail.com" SUBJECT "abcde" BODY "123456789" UID 9999:*)

def get_first_text_block(msg):
    type = msg.get_content_maintype()

    if type == 'multipart':
        for part in msg.get_payload():
            if part.get_content_maintype() == 'text':
                return part.get_payload()
    elif type == 'text':
        return msg.get_payload()





@app.route('/sendtext/<id>', methods=['POST', 'GET'])
def sendtext(id):
    print("-----------------")
    print(id+"\n")
    cursor = posts.find({'_id': ObjectId(id)})
    temp = dict()
    for i in cursor:
        temp = i
    print(temp)
    tList = []
    for k,v in temp.items():
        tList.append((k,v))
    return render_template('sendtext.html', info = tList)


@app.route('/sendtextmail/<id>', methods=['POST', 'GET'])
def sendtextmail(id):
    print("-----------------")
    print(id)
    #id.replace("%40","@")
    cursor = posts.find({'_id': ObjectId(id.replace(',',""))})
    temp = dict()
    for i in cursor:
        temp = i
    print(temp)
    tList = []
    for k,v in temp.items():
        tList.append((k,v))

    smtp_ssl_host = 'smtp.gmail.com'  # smtp.mail.yahoo.com
    smtp_ssl_port = 465
    username = tList[6][1]
    password = tList[7][1]
    sender = tList[6][1]
    targets = request.form['sendto']

    msg = MIMEText(request.form['textmail'])
    msg['Subject'] =request.form['subject']
    msg['From'] = sender
    msg['To'] = ', '.join(targets)

    server = smtplib.SMTP_SSL(smtp_ssl_host, smtp_ssl_port)
    server.login(username, password)
    server.sendmail(sender, targets, msg.as_string())
    server.quit()

    return render_template('userinformation.html', info=tList)
if __name__ == '__main__':
    app.run()
