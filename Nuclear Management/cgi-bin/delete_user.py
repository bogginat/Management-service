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
num = form.getfirst("login", "")

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

    info.pop(num)
    passwords_adm.pop(num)

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
