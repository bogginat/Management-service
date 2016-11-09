#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Import modules for CGI handling


import cgi, cgitb
import json, codecs
import datetime
import math
import http.cookies
import os

# Create instance of FieldStorage
form = cgi.FieldStorage()

# Get data from fields
firstname = form.getvalue('firstname')
lastname = form.getvalue('lastname')
surname = form.getvalue('surname')
job = form.getvalue('job')
login = form.getvalue('login')
num = form.getvalue('num')
passw = form.getvalue('passw')
adm = form.getvalue('adm')


from _wall import Wall
wall = Wall()

cookie = http.cookies.SimpleCookie(os.environ.get("HTTP_COOKIE"))
session = cookie.get("session")
if session is not None:
    session = session.value
user = wall.find_cookie(session)  # Ищем пользователя по переданной куке


if wall.adminust(user):
    inp = codecs.open('users/users.json', 'r') #пароли и админство
    passwords = inp.read()
    passwords_adm = json.loads(passwords)
    inp.close()

    inp = codecs.open('data_users/data_users.json', 'r') #личная инфа
    inform = inp.read()
    info = json.loads(inform)
    inp.close()

    if wall.find1(login) and login == num:
        passwords_adm[login][0] = passw
        info[login][1] = firstname
        info[login][0] = surname
        info[login][2] = lastname
        info[login][3] = job
        passwords_adm[login][1] = adm


        passwords1 = json.dumps(passwords_adm)
        inform1 = json.dumps(info)

        outp = codecs.open('users/users.json', 'w') #пароли и админство
        outp.write(passwords1)
        inp.close()

        outp = codecs.open('data_users/data_users.json', 'w') #личная инфа
        outp.write(inform1)
        inp.close()

        print ("Content-type:text/html; charset=utf-8\n\n")
        print ("<html>")
        print ("<head>")
        print ("<title>Find</title>")
        print ('<meta http-equiv="refresh" content="0; url="http:/cgi-bin/users_adm.py" />')
        print ('<script type="text/javascript"> window.location.href = "http:/cgi-bin/users_adm.py" </script>')
        print ("</head>")
        print ("<body bgcolor = #A8EEF5>")
        print ("</body>")
        print ("</html>")

    elif wall.find1(login) and login != num:

        print ("Content-type:text/html; charset=utf-8\n\n")
        print ("<html>")
        print ("<head>")
        print ("<title>Ошибка</title>")
        print('<link type="text/css" rel="stylesheet" href="/stylesheets/main.css" />')
        print ("</head>")
        print ("<body>")
        print('<form align ="right" action="/cgi-bin/wall.py">')
        print('<input type="submit" class ="button" value="Вернуться">')
        print('</form>')
        print("Пользователь с таким логином уже существует. Изменения не сохранены.")
        print ("</body>")
        print ("</html>")

    else:
        info.pop(num)
        passwords_adm.pop(num)
        passwords_adm[login][0] = passw
        info[login][1] = firstname
        info[login][0] = surname
        info[login][2] = lastname
        info[login][3] = job
        passwords_adm[login][1] = adm

        passwords1 = json.dumps(passwords_adm)
        inform1 = json.dumps(info)

        outp = codecs.open('users/users.json', 'w') #пароли и админство
        outp.write(passwords1)
        inp.close()

        outp = codecs.open('data_users/data_users.json', 'w') #личная инфа
        outp.write(inform1)
        inp.close()

        print ("Content-type:text/html; charset=utf-8\n\n")
        print ("<html>")
        print ("<head>")
        print ("<title>Find</title>")
        print ('<meta http-equiv="refresh" content="0; url="http:/cgi-bin/users_adm.py" />')
        print ('<script type="text/javascript"> window.location.href = "http:/cgi-bin/users_adm.py" </script>')
        print ("</head>")
        print ("<body bgcolor = #A8EEF5>")
        print ("</body>")
        print ("</html>")

else:
    pattern = '''
<!DOCTYPE HTML>
<html>
<head>
<meta charset="utf-8">
  <meta http-equiv="refresh" content="0; url="http:/cgi-bin/wall.py" />
  <script type="text/javascript"> window.location.href = "http:/cgi-bin/wall.py" </script>
</head>
</html>
'''
    print(pattern)
