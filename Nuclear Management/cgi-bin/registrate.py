#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cgi
import http.cookies
import os
import json, codecs

from _wall import Wall
wall = Wall()

cookie = http.cookies.SimpleCookie(os.environ.get("HTTP_COOKIE"))
session = cookie.get("session")
if session is not None:
    session = session.value
user = wall.find_cookie(session)  # Ищем пользователя по переданной куке


if wall.adminust(user):
    pub1 = '''
<!DOCTYPE HTML>
<html>
<head>
<meta charset="utf-8">
<title>Регистрация</title>
  <link type="text/css" rel="stylesheet" href="/stylesheets/main.css" />
</head>
<body>
    '''
    print('Content-type: text/html\n')
    print(pub1)
    print('Пользователь:{}'.format(user))
    print('<form align ="right" action="/cgi-bin/wall.py">')
    print('<input type="text" name="text" class ="area_logout" value = {}>'.format(session))
    print('<input type="hidden" name="action" value="logout">')
    print('<input class ="button" type="submit" value="Выйти">')
    print('</form>')
    pub = '''
    <!DOCTYPE HTML>
   <form align = "right" action="/cgi-bin/users_adm.py">
        <input type="submit" class ="button" value="Пользователи">
    </form>
    <form align ="right" action="/cgi-bin/wall.py">
    <input type="submit" class ="button" value="Вернуться">
    </form>
Форма для регистрации:<p>
    <form action="/cgi-bin/wall.py">
        Фамилия:   <input type="text" name="fam"><br><br>
        Имя:       <input type="text" name="im"><br><br>
        Отчество:  <input type="text" name="otch"><br><br>
        Должность: <input type="text" name="job"><br><br>
        Логин:     <input type="text" name="login"><br><br>
        Пароль:    <input type="password" name="password"><br><br>
        Администратор: <input type=checkbox name="adm" value="yes"><br><br>
        <input type="hidden" name="action" value="reg">
        <input type="submit" class ="button" value="Зарегистрировать">
    </form>
<style>
.button {
    position: relative;
	background: white;
	border: 2px solid #c2e1f5;
}
</style>
</body>
</html>
'''
    print(pub)

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
