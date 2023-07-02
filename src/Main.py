# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__ = "home"
__date__ = "$26 Apr, 2021 6:30:58 PM$"

from flask import Flask
from flask import flash
from flask import render_template
from flask import request
from flask import session
from flask import redirect
from flask import url_for
import os
import pymysql
from werkzeug.utils import secure_filename

import plotly.graph_objects as go
from plotly import subplots
import pandas as pd
import plotly.express as px
import numpy as np
from dash.dependencies import Input, Output, State
import cv2
import PIL.Image as image
from io import BytesIO
import base64
from matplotlib import pyplot as plt
from libr import dnn_classification
#project explanation
import pickle

#project explanation
from IPython.display import display, Image



		 
from tensorflow.keras.models import load_model
dnnclassification = load_model('finalized_model_DNN.h5')


#initialisig the values
classification = {"Slender":0, "Medium":0, "Bold":0, "Round":0, "Dust":0}
avg = {"Slender":0, "Medium":0, "Bold":0, "Round":0, "Dust":0}

UPLOAD_FOLDER = 'D:/uploads'
ALLOWED_EXTENSIONS = set(["jpg", "jpeg", "tif", "tiff", "png","PNG"])

app = Flask(__name__)
app.secret_key = "1234"
app.password = ""
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
class Database:
    def __init__(self):
        host = "localhost"
        user = "root"
        password = ""
        db = "ricedetection"
        self.con = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.DictCursor)
        self.cur = self.con.cursor()
    def getuserprofiledetails(self, username):
        strQuery = "SELECT PersonId,Firstname,Lastname,Phoneno,Address,Recorded_Date FROM personaldetails WHERE Username = '" + username + "' LIMIT 1"
        self.cur.execute(strQuery)
        result = self.cur.fetchall()
        print(result)
        return result
    def insertpersonaldetails(self, firstname, lastname, phone, email, address, username, password):
        print('insertpersonaldetails::' + username)
        strQuery = "INSERT INTO personaldetails(Firstname, Lastname, Phoneno, Emailid, Address, Username, Password, Recorded_Date) values(%s, %s, %s, %s, %s, %s, %s, now())"
        strQueryVal = (firstname, lastname, phone, email, address, username, password)
        self.cur.execute(strQuery, strQueryVal)
        self.con.commit()
        return ""
    def getpersonaldetails(self, username, password):
        strQuery = "SELECT COUNT(*) AS c, PersonId FROM personaldetails WHERE Username = '" + username + "' AND Password = '" + password + "'"        
        self.cur.execute(strQuery)        
        result = self.cur.fetchall()       
        return result
    def getuserpersonaldetails(self, name):
        strQuery = "SELECT PersonId, Firstname, Lastname, Phoneno, Address, Recorded_Date FROM personaldetails WHERE Username = '" + name + "' "
        self.cur.execute(strQuery)
        result = self.cur.fetchall()
        print(result)
        return result
    def getuploaddetails(self):
        strQuery = "SELECT UploadId, PersonId, ImagePath, OPImagePath1, OPImagePath2, OPImagePath3, Results, Recorded_Date "
        strQuery += "FROM uploaddetails "
        strQuery += "ORDER BY Recorded_Date DESC "
        strQuery += "LIMIT 1"
        self.cur.execute(strQuery)
        result = self.cur.fetchall()
        print(result)
        return result
    def getimagedetails(self, imgId):
        strQuery = "SELECT ImagePath, OPImagePath1, OPImagePath2, OPImagePath3 "
        strQuery += "FROM uploaddetails "
        strQuery += "WHERE UploadId = (%s) "
        strQueryVal = str(imgId)
        self.cur.execute(strQuery, strQueryVal)
        result = self.cur.fetchall()
        print(result)
        return result
    def insertuploaddetails(self, PersonId, ImagePath, OPImagePath1, OPImagePath2, OPImagePath3, Results):
        strQuery = "INSERT INTO uploaddetails(PersonId, ImagePath, OPImagePath1, OPImagePath2, OPImagePath3, Results, Recorded_Date) values(%s, %s, %s,%s, %s, %s, now())"
        strQueryVal = (str(PersonId), str(ImagePath), str(OPImagePath1), str(OPImagePath2), str(OPImagePath3), str(Results))
        self.cur.execute(strQuery, strQueryVal)
        self.con.commit()
        return ""
        
@app.route('/', methods=['GET'])
def loadindexpage():
    return render_template('index.html')

@app.route('/index', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/codeindex', methods=['POST'])
def codeindex():
    username = request.form['username']
    password = request.form['password']
    
    print('username:' + username)
    print('password:' + password)
    
    try:
        if username is not "" and password is not "": 
            def db_query():
                db = Database()
                emps = db.getpersonaldetails(username, password)       
                return emps
            res = db_query()
            
            for row in res:
                print(row['c'])
                count = row['c']
                
                if count >= 1:      
                    session['x'] = username;
                    session['UID'] = row['PersonId'];
                    def db_query():
                        db = Database()
                        emps = db.getuserprofiledetails(username)       
                        return emps
                    profile_res = db_query()
                    return render_template('userprofile.html', sessionValue=session['x'], result=profile_res, content_type='application/json')
                else:
                    flash ('Incorrect Username or Password.')
                    return render_template('index.html')
        else:
            flash ('Please fill all mandatory fields.')
            return render_template('index.html')
    except NameError:
        flash ('Due to technical problem, your request could not be processed.')
        return render_template('index.html')
        
    return render_template('index.html')

@app.route('/usersignin', methods=['GET'])
def usersignin():
    return render_template('usersignin.html')

@app.route('/codeusersignin', methods=['POST'])
def codeusersignin():
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    phone = request.form['phone']
    email = request.form['email']
    address = request.form['address']    
    username = request.form['username']
    password = request.form['password']
    
    print('firstname:', firstname)
    print('lastname:', lastname)
    print('phone:', phone)
    print('email:', email)
    print('address:', address)
    print('username:', username)
    print('password:', password)
    
    try:
        if firstname is not "" and lastname is not ""  and phone is not "" and email is not "" and address is not "" and username is not "" and password is not "": 
            def db_query():
                db = Database()
                emps = db.getpersonaldetails(username, password)       
                return emps
            res = db_query()

            for row in res:
                print(row['c'])
                count = row['c']

                if count >= 1:      
                    flash ('Entered details already exists.')
                    return render_template('usersignin.html')
                else:
                    def db_query():
                        db = Database()
                        emps = db.insertpersonaldetails(firstname, lastname, phone, email, address, username, password)    
                        return emps
                res = db_query()
                flash ('Dear Customer, Your registration has been done successfully.')
                return render_template('index.html')
        else:                        
            flash ('Please fill all mandatory fields.')
            return render_template('usersignin.html')
    except NameError:
        flash ('Due to technical problem, your request could not be processed.')
        return render_template('usersignin.html')
    
    return render_template('usersignin.html')

@app.route('/userprofile', methods=['GET'])
def userprofile():
    def db_query():
        db = Database()
        emps = db.getuserpersonaldetails(session['x'])       
        return emps
    profile_res = db_query()
    return render_template('userprofile.html', sessionValue=session['x'], result=profile_res, content_type='application/json')

@app.route('/signout', methods=['GET'])
def signout():    
    return render_template('signout.html')

@app.route('/logout', methods=['GET'])
def logout():
    del session['x']
    return render_template('index.html')

@app.route('/uploaddata', methods=['GET'])
def uploaddata():
    return render_template('uploaddata.html', sessionValue=session['x'], content_type='application/json')

@app.route("/codeuploaddata", methods=["POST"])
def codeuploaddata():

    file = request.files["filepath"]

    print("filename:" + file.filename)
	
    if "filepath" not in request.files:

        flash("Please fill all mandatory fields.")
        return render_template("uploaddata.html", content_type="application/json")

    else:
    
        if file.filename != "" :

            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

                filepath = UPLOAD_FOLDER + "/" + file.filename
                print("filepath:" + filepath)
                import cv2
                import numpy as np
                from matplotlib import pyplot as plt
                img = cv2.imread(filepath)
                print(img)
                hist,bins = np.histogram(img.flatten(),256,[0,256])

                cdf = hist.cumsum()
                cdf_normalized = cdf * hist.max()/ cdf.max()



                #convert into binary
                if len(img.shape)==3:
                    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
                # 160 - threshold, 255 - value to assign, THRESH_BINARY_INV - Inverse binary
                ret,binary = cv2.threshold(img,160,255,cv2.THRESH_BINARY)

                #averaging filter
                kernel = np.ones((5,5),np.float32)/9
                dst = cv2.filter2D(binary,-1,kernel)
                # -1 : depth of the destination image
                kernel2 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))

                #erosion
                erosion = cv2.erode(dst,kernel2,iterations = 1)

                #dilation
                dilation = cv2.dilate(erosion,kernel2,iterations = 1)

                #edge detection
                edges = cv2.Canny(dilation,100,200)

                #size detection cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
                contours, hierarchy = cv2.findContours(erosion, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                print("No. of grains=",len(contours))
                total_ar=0
                count=0
                s=0
                r=0
                b=0
                d=0
                m=0
                #counting impurities
                for cnt in contours:
                    x,y,w,h = cv2.boundingRect(cnt)
                    aspect_ratio = float(w)/h
                    if(aspect_ratio<1):
                        aspect_ratio=1/aspect_ratio
                    #print(round(aspect_ratio,2),get_classification(aspect_ratio))
                    clas=dnn_classification(aspect_ratio)
                    temp =img[y:y+h,x:x+w]
                    
                    if clas=="Slender":
                        cv2.imwrite('./data/Slender/'+str(count)+'.jpg',temp)
                        s+=1
                    if clas== "Medium":
                        cv2.imwrite('./data/Medium/'+str(count)+'.jpg',temp)
                        m+=1
                    if clas=="Bold":
                        cv2.imwrite('./data/Bold/'+str(count)+'.jpg',temp)
                        b+=1
                    if clas=="Round":
                        cv2.imwrite('./data/Round/'+str(count)+'.jpg',temp)
                        r+=1
                    if clas=="Dust":
                        cv2.imwrite('./data/Dust/'+str(count)+'.jpg',temp)
                        d+=1
                    count+=1
                    

                print("Slender Count:"+str(s))
                print("Medium Count:"+str(m))
                print("Bold Count:"+str(b))
                print("Round Count:"+str(r))
                print("Dust Count:"+str(d))
                #saving different types of images
                cv2.imwrite("img.jpg", img)
                cv2.imwrite(UPLOAD_FOLDER + '/1.png', binary)
                cv2.imwrite(UPLOAD_FOLDER + '/2.png', dst)
                cv2.imwrite("erosion.jpg", erosion)
                cv2.imwrite("dilation.jpg", dilation)
                cv2.imwrite(UPLOAD_FOLDER + '/3.png', edges)


                xc=[s,m,b,r,d]

                if np.argmax(xc)==0:
                    output="No. of grains="+str(len(contours)) +' And Highest Count is:'+str(s)+'( Slender)'
                elif np.argmax(xc)==1:
                    output="No. of grains="+str(len(contours)) +' And Highest Count is:'+str(m)+'( Medium)'
                elif np.argmax(xc)==2:
                    output="No. of grains="+str(len(contours)) +' And Highest Count is:'+str(b)+'( Bold )'
                elif np.argmax(xc)==3:
                    output="No. of grains="+str(len(contours)) +' And Highest Count is:'+str(r)+'( Round)'
                elif np.argmax(xc)==4:
                    output="No. of grains="+str(len(contours)) +' And Highest Count is:'+str(d)+'( Dust)'
                else:
                    output="No. of grains="+str(len(contours)) +' And None Type'
                    
                print(output)
                
                db = Database()
                db.insertuploaddetails(session['UID'], file.filename, '1.png', '2.png', '3.png', output)

                flash("File successfully uploaded, Kindly view the analyzed result's!")
                return redirect(url_for("viewuploadeddata"))

            else:
                flash("Allowed file types are .csv")
                return render_template("uploaddata.html", content_type="application/json")
        else:
            flash("Please fill all mandatory fields.")
            return render_template("uploaddata.html", content_type="application/json")


@app.route("/viewuploadeddata", methods=["GET"])
def viewuploadeddata():
    def db_query():
        db = Database()
        emps = db.getuploaddetails()
        return emps

    profile_res = db_query()
    return render_template("viewuploadeddata.html", result=profile_res, content_type="application/json")

@app.route("/fetchIPImg/<int:imgId>")
def fetchIPImg(imgId):
    def db_query():
        db = Database()
        emps = db.getimagedetails(imgId)
        return emps

    profile_res = db_query()

    filename = ""

    for row in profile_res:
        filename = row["ImagePath"]
        print(filename)

    from flask import send_from_directory

    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

@app.route("/fetchOPImg1/<int:imgId>")
def fetchOPImg1(imgId):
    def db_query():
        db = Database()
        emps = db.getimagedetails(imgId)
        return emps

    profile_res = db_query()

    filename = ""

    for row in profile_res:
        filename = row["OPImagePath1"]
        print(filename)

    from flask import send_from_directory

    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

@app.route("/fetchOPImg2/<int:imgId>")
def fetchOPImg2(imgId):
    def db_query():
        db = Database()
        emps = db.getimagedetails(imgId)
        return emps

    profile_res = db_query()

    filename = ""

    for row in profile_res:
        filename = row["OPImagePath2"]
        print(filename)

    from flask import send_from_directory

    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

@app.route("/fetchOPImg3/<int:imgId>")
def fetchOPImg3(imgId):
    def db_query():
        db = Database()
        emps = db.getimagedetails(imgId)
        return emps

    profile_res = db_query()

    filename = ""

    for row in profile_res:
        filename = row["OPImagePath3"]
        print(filename)

    from flask import send_from_directory

    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

if __name__ == "__main__":
    app.run(debug=False,host='0.0.0.0')