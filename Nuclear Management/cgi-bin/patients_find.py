#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Import modules for CGI handling
import cgi, cgitb
import json, codecs
import http.cookies
import os


from _wall import Wall
wall = Wall()

cookie = http.cookies.SimpleCookie(os.environ.get("HTTP_COOKIE"))
session = cookie.get("session")
if session is not None:
    session = session.value
user = wall.find_cookie(session)  # Ищем пользователя по переданной куке


# Create instance of FieldStorage
form_f = cgi.FieldStorage()

# Get data from fields
FIO = form_f.getvalue('firstname_f')

if user is not None:
    print ("Content-type:text/html; charset=utf-8\n\n")
    print ("<html>")
    print ("<head>")
    print ("<title>Найти</title>")
    print('<link type="text/css" rel="stylesheet" href="/stylesheets/main.css" />')
    print ("</head>")
    print ("<body>")
    print('Пользователь:{}'.format(user))
    print('<p>')
    print('<form align ="right" action="/cgi-bin/wall.py">')
    print('<input type="submit" class ="button" value="Вернуться">')
    print('</form>')

    inp = codecs.open('patients.txt', 'r')
    text = inp.read()
    patients = json.loads(text)
    inp.close()

    date = "нет совпадений"
    firstname = "нет совпадений"
    surname = "нет совпадений"
    lastname = "нет совпадений"
    w = "нет совпадений"
    m = 0
    k = 0
    for elem in patients:
        s = elem[2]
        s_1 = s
        if s_1 == FIO:
            date = elem[0]
            firstname = elem[1]
            surname = elem[2]
            lastname = elem[3]
            w = elem[4]
            hb = elem[5]
            num = k
            print ('<form align = "left" action="/cgi-bin/reload.py" method="get" name = "form" id = "format">')
            print ('Дата:<br><input type="text" name="date" id="date" value = "{}"><br>'.format(date))
            print ('Имя:<br><input type="text" name="firstname" value = "{}"><br>'.format(firstname))
            print ('Фамилия:<br><input type="text" name="surname" value = "{}"><br>'.format(surname))
            print ('Отчество:<br><input type="text" name="lastname" value = "{}"><br>'.format(lastname))
            print ('Дата рождения:<br><input type="text" name="hb" value = "{}"><br>'.format(hb))
            print ('Вес:<br><input type="text" name="w" value = "{}"><br>'.format(w))
            print ('<br><input type="text" name="num" value = "{}" class = "n">'.format(num))
            print ('<input type="submit" class = "button" value="Сохранить данные">')
            print ('</form>')
            print ('<form align = "left" action="/cgi-bin/delete.py" method="get" name = "form" id = "format">')
            print ('<input type="text" name="num" value = "{}" class = "n">'.format(num))
            print ('<input type="submit" class = "button" value="Удалить пациента">')
            print ('</form>')
            m+=1
        k = k + 1
    if m != 0:
        print("Больше людей с фамилией {} не найдено.".format(FIO))
    else:
        print("Не найдено людей c фамилией {}.".format(FIO))
    print ("</body>")
    print('<style> .n {visibility: hidden; display: none;} </style>')
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

