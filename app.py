from flask import Flask, request , render_template , redirect , url_for , session
# import json
import sqlite3
import os
import pyqrcode
import png
# from pyqrcode import QRCode
# import random
# import string
# import socket   
from flask import Flask,request
from flask import send_file

app = Flask(__name__)

def db_connection():
    conn = None
    try:
        conn = sqlite3.connect("hospital.sqlite")
    except sqlite3.error as e:
        print(e)
    return conn

@app.route('/',methods=['GET','POST'])
def index():
    conn = db_connection() 
    cursor = conn.cursor()
    if request.method == 'POST':
        Email = request.form['Email']
        password = request.form['password']
        patient_data = cursor.execute("SELECT * FROM patient WHERE Email = ? AND password = ?", (Email, password))
        patient_data = cursor.fetchall()
        for x in patient_data:
            session['id'] = x[0]
        session['logged_in'] = True
        if patient_data:
            if session['logged_in'] == True:
                return redirect("/data?id="+str(session['id']))
            print('logged in')
    return render_template('index.html')

@app.route('/login',methods=['GET','POST'])
def login():
    conn = db_connection() 
    cursor = conn.cursor()
    if request.method == 'POST':
        Email = request.form['Email']
        password = request.form['password']
        patient_data = cursor.execute("SELECT * FROM patient WHERE Email = ? AND password = ?", (Email, password))
        patient_data = cursor.fetchall()
        for x in patient_data:
            session['id'] = x[0]
        session['logged_in'] = True
        if patient_data:
            if session['logged_in'] == True:
                return redirect("/data?id="+str(session['id']))
            print('logged in')
    return render_template('index.html')

@app.route('/applogin',methods=['GET','POST'])
def applogin():
    if request.method == 'GET':
        username=request.args.get('email')
        password=request.args.get('password')
        conn = db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM patient WHERE Email = ? AND password = ?", (username, password))
        patient_data = cursor.fetchall()
        if len(patient_data)>0:
            return "success"

@app.route('/data',methods=['GET','POST'])
def data():
    if request.method == 'GET':
        id = request.args.get('id')
        conn = db_connection()
        cursor = conn.cursor()
        patient_data = cursor.execute("SELECT * FROM patient WHERE id = ?", (id))
        patient_data = cursor.fetchall()
        print(patient_data)
    return render_template('data.html', patient_data=patient_data , id=id)

@app.route('/temp1',methods=['GET','POST'])
def temp1():
    if request.method == 'GET':
        id = request.args.get('id')
        conn = db_connection()
        cursor = conn.cursor()
        med_data = cursor.execute("SELECT * FROM medicinedetails WHERE id = 1")
        med_data = cursor.fetchall()
        return str(med_data[0][4])

@app.route('/temp2',methods=['GET','POST'])
def temp2():
    if request.method == 'GET':
        conn = db_connection()
        cursor = conn.cursor()
        med_data = cursor.execute("SELECT * FROM medicinedetails WHERE id = 2")
        med_data = cursor.fetchall()
        return str(med_data[0][4])

@app.route('/temp3',methods=['GET','POST'])
def temp3():
    if request.method == 'GET':
        conn = db_connection()
        cursor = conn.cursor()
        med_data = cursor.execute("SELECT * FROM medicinedetails WHERE id =3")
        med_data = cursor.fetchall()
        return str(med_data[0][4])

@app.route('/timer',methods=['GET','POST'])
def timer():
    if request.method == 'GET':
        a=1
        id = request.args.get('id')
        print(type(id))
        conn = db_connection()
        cursor = conn.cursor()
        med_data = cursor.execute("SELECT * FROM medicinedetails ")
        med_data = cursor.fetchall()
        if int(id)==1:
            a=2
        elif int(id)==2:
            a=3
        elif int(id)==3:
            a=4
        else:
            a=1
        return str(a)



@app.route('/dataadd', methods=['GET','POST'])
def dataadd():
    conn = db_connection() 
    cursor = conn.cursor()
    if request.method == "POST":
        Name = request.form["Name"]
        Address = request.form["Address"]
        Pin = request.form["Pin"]
        DOB = request.form["DOB"]
        BloodGroup = request.form["BloodGroup"]
        ContactNumber = request.form["ContactNumber"]
        EmergencyContactNumber = request.form["EmergencyContactNumber"]
        Email = request.form["Email"]
        password = request.form["password"]
        sql = """INSERT INTO patient (Name, Address, Pin, DOB, BloodGroup, ContactNumber, EmergencyContactNumber,Email,password) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        cursor = cursor.execute(sql, (Name, Address, Pin, DOB, BloodGroup, ContactNumber, EmergencyContactNumber, Email, password))
        cursor.execute("SELECT * FROM patient WHERE Email = ? AND password = ?", (Email, password))
        patient_data = cursor.fetchall()
        for x in patient_data:
            session['id'] = x[0]
        if patient_data:
            cursor.execute("UPDATE patient SET image = ? WHERE id = ?", (qrfile, session['id']))
        conn.commit()
        return redirect(url_for('index'))
    return render_template('dataadd.html')

@app.route('/ViewQR/<id>', methods=['GET','POST'])
def ViewQR(id):
    if request.method == "GET":
        conn = db_connection() 
        cursor = conn.cursor()
        print(id)
        cursor.execute("SELECT * FROM patient WHERE id = ?", (id))
        patient_data = cursor.fetchall()
        for x in patient_data:
            qrfile = x[10]
        print(qrfile)
        return send_file(qrfile, mimetype='image/svg+xml')
    return render_template('ViewQR.html')

@app.route('/logout')
def logout():
    session['id'] = None
    return redirect(url_for('index'))

@app.route('/medinedata', methods=['GET','POST'])
def medinedata():
    if request.method == 'GET':
        conn = db_connection()
        cursor = conn.cursor()
        patient_data = cursor.execute("SELECT * FROM medicinedetails ")
        patient_data = cursor.fetchall()
        

@app.route("/deletepatient/<int:id>", methods=["GET", "POST"])
def deletepatient(id):
    conn = db_connection()
    cursor = conn.cursor()
    if request.method == "POST":
        sql = """DELETE FROM patient WHERE id=?"""
        cursor = cursor.execute(sql, (id,)) 
        conn.commit()
        return f"Patient data with id {id} deleted successfully"

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True, host="0.0.0.0" , port=8000)
