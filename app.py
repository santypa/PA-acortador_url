import re
from sqlite3 import Cursor
from flask import Flask, render_template, request, redirect, url_for

import mysql.connector
import pyshorteners

import string
import random






app = Flask(__name__)

# academia.c1mebdhdxytu.us-east-1.rds.amazonaws.com
# usuario :  p4
# ALrUBIaLYcHR
db = mysql.connector.connect(
    host='localhost',
    user="root",
    password="",
    database="acortadores",
    port="3306"
)
db.autocommit = True

@app.get("/")
def acortar():
    
    cursor = db.cursor(buffered=True)
    cursor.execute("SELECT * FROM  urls ORDER BY id DESC")
    forms = cursor.fetchone()
    
    
    if forms == None:
        val = 0
        val2 = 0
    else:
        
        val = 1
        val2 = forms[0]
        
    cursor.close()
    return render_template("inicio.html", forms=forms, val=val, val2=val2)

@app.post("/")
def acortarPost():
    puerto = request.form.get('nurl')
    
    for x in range(5):
        code= (''.join(random.choice(string.ascii_letters + string.digits) for _ in range(5)))
        
    forma = request.host_url+code
    cursor = db.cursor()
    cursor.execute("INSERT INTO urls(puerto,forma) VALUES (%s,%s)", (
        puerto,
        forma
    ))

    cursor.close()
    return redirect(url_for("acortar"))

@app.route("/<url>")
def cortarRoute(url):
    url = request.host_url+url
    cursor = db.cursor()
    cursor.execute("SELECT puerto FROM urls WHERE forma = %s",(url,))
    url = cursor.fetchone()
    
    if(url != None): return redirect(url[0])
    return redirect(url_for("acortar"))

    #   url = forms[2]
    # cursor.execute("SELECT puerto FROM urls WHERE forma = %s",(url))

app.run(debug=True)
