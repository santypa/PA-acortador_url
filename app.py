import re
from sqlite3 import Cursor
from flask import Flask, render_template, request, redirect, url_for

import mysql.connector
import pyshorteners

app = Flask(__name__)

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
    # cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM  urls ORDER BY id DESC")
    forms = cursor.fetchone()
    # resultado=cursor.fetchone()
    # print (resultado)

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
    url = puerto
    shrt = pyshorteners.Shortener()
    forma = shrt.tinyurl.short(url)
    # print(forma)

    cursor = db.cursor()
    cursor.execute("INSERT INTO urls(puerto,forma) VALUES (%s,%s)", (
        puerto,
        forma
    ))

    cursor.close()
    return redirect(url_for("acortar"))

app.run(debug=True)
