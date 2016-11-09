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

if wall.adminust(user):

    pub = '''
    <!DOCTYPE HTML>
    <html>
    <head>
    <meta charset="utf-8">
    <title>Пользователи</title>
    <link type="text/css" rel="stylesheet" href="/stylesheets/main.css" />
    </head>
    '''
    print(pub)
    print('<body>')
    print('Пользователь:{}'.format(user))
    print('<form align ="right" action="/cgi-bin/wall.py">')
    print('<input type="text" name="text" class ="area_logout" value = {}>'.format(session))
    print('<input type="hidden" name="action" value="logout">')
    print('<input type="submit" class ="button" value="Выйти">')
    print('</form>')
    print('<form align ="right" action="/cgi-bin/registrate.py">')
    print('<input type="submit" class ="button" value="Вернуться">')
    print('</form>')
    pub1 = '''
    <style>
    .area_logout{visibility: hidden;}
    </style>
    '''
    print(pub1)

    inp = codecs.open('users/users.json', 'r') #пароли и админство
    passwords = inp.read()
    passwords_adm = json.loads(passwords)
    inp.close()

    inp = codecs.open('data_users/data_users.json', 'r') #личная инфа
    inform = inp.read()
    info = json.loads(inform)
    inp.close()


    k = 0
    for key in passwords_adm:
        num = k
        passw = passwords_adm[key][0]
        login = key
        firstname = info[key][1]
        surname = info[key][0]
        lastname = info[key][2]
        job = info[key][3]
        print ('<form action="/cgi-bin/reload_user.py" method="get" name = "form" id = "format">')
        print ('Имя:<input type="text" name="firstname" value = "{}"><br><br>'.format(firstname))
        print ('Фамилия:<input type="text" name="surname" value = "{}"><br><br>'.format(surname))
        print ('Отчество:<input type="text" name="lastname" value = "{}"><br><br>'.format(lastname))
        print ('Логин:<input type="text" name="login" value = "{}"><br><br>'.format(login))
        print ('Пароль:<input type="text" name="passw" value = "{}"><br><br>'.format(passw))
        print ('Должность:<input type="text" name = "job" value = "{}"><br><br>'.format(job))
        if passwords_adm[key][1] == "yes":
            print('<input type=checkbox name="adm" value="yes" checked>Администратор<br>')
        else:
            print('<input type=checkbox name="adm" value="yes">Администратор<br>')
        print ('<input type="text" name="num" value = "{}" class = "n">'.format(login))
        print ('<input type="submit" class ="button" value="Сохранить данные">')
        print ('</form>')
        print ('<form action="/cgi-bin/delete_user.py" method="get" name = "form" id = "format"><input type="text" name="login" value = "{}" class = "n">'.format(login))
        print ('<input type="submit" class ="button" value="Удалить пользователя">')
        print ('</form>')
        print('<p> </p>')
        k = k + 1
    print('</body>')
    print('<style> .n {visibility: hidden; display: none;} </style>')
    print('</html>')

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
