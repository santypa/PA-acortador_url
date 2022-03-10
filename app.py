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
    cursor = db.cursor(dictionary=True)
    cursor.execute("select * from urls")
    forms = cursor.fetchall()
    if forms == None:
        val = 0
    else:
        val = 1
    cursor.close()
    return render_template("inicio.html", forms=forms, val=val)


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
    print("bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb")
    
    return redirect(url_for("acortar"))

# @app.delete("/")
# def acortarPos():
#     puerto = request.form.get('nurl')
#     #id= request.form.get('id')
#     url = puerto
#     shrt = pyshorteners.Shortener()
#     forma = shrt.tinyurl.short(url)
#     cursor = db.cursor()
    
#     cursor.execute("INSERT INTO urls(puerto,forma) VALUES (%s,%s)", (
#         puerto,
#         forma
#     ))
#     cursor.close()
#     print("ccccccccccccccccccccccccccccccccccccccccccccccccccccccccc")
#     return redirect(url_for("acortar"))
      


#@app.delete("/")
#def acortarDel():
   # id = request.form.get('id')
   # val = id
   # cursor = db.cursor()
   # cursor.execute("DELETE FROM acortadores. urls WHERE (id=%s)", (
   #     id,
   # ))
    
    #cursor.close
    #print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
    #return render_template("ini.html", val=val)


app.run(debug=True)
