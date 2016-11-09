#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cgi
import http.cookies
import os
import datetime
import math
import json, codecs


from _wall import Wall
wall = Wall()

cookie = http.cookies.SimpleCookie(os.environ.get("HTTP_COOKIE"))
session = cookie.get("session")
if session is not None:
    session = session.value
user = wall.find_cookie(session)  # Ищем пользователя по переданной куке

form = cgi.FieldStorage()
action = form.getfirst("action", "")

if action == "change" and wall.adminust(user):

    ndate = form.getfirst("ndate", "")

    start = ndate.split('-')

    inp = codecs.open('fill/fill.json', 'r')
    text = inp.read()
    fills = json.loads(text)
    inp.close()

    fills[0] = ndate #пока одна загрузка

    json_fill = json.dumps(fills)

    outp = open('fill/fill.json', 'w')
    outp.write(json_fill)
    outp.close()

    inp = codecs.open('times.txt', 'r')
    text = inp.read()
    data = json.loads(text)
    inp.close()

    weight = {}

    for elem in data:
        weight[elem] = 0

    inp = codecs.open('patients.txt', 'r')
    text = inp.read()
    patients = json.loads(text)
    inp.close()

    for elem in patients:
        s = elem[0]
        weight[s] += int(elem[4])


    week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    day_of_load = datetime.date(int(start[0]), int(start[1]), int(start[2]))
    count_load = 0
    day_of_week = 0 #номер дня недели
    inaccuracy = float(1.27) #погрешность
    doze = float(0.035) #дозировка
    average_weight = 76 #средний вес

    inp = open('data.txt', 'r') #взяли гбк на каждые 3ие сутки
    data = inp.readlines()
    Gbq_Ml = []
    Gbq = []
    for i in data:
        Gbq_Ml.append(float(i.split('\t')[-1].split('\n')[0]))
        Gbq.append(float(i.split('\t')[-2].split('\n')[0]))

    def opportunity(weight, day, inaccuracy, doze, weight_pat): #посчитали, реально ли кого-то уколоть
        return Gbq_Ml[day // 3] >= (inaccuracy * weight * doze) / 2

    def opportunity_people(weight, day, inaccuracy, doze, weight_pat):#посчитали, скольких мы можем уколоть
        return opportunity(weight, day, inaccuracy, doze, weight_pat) * math.floor((Gbq[day // 3] - inaccuracy * doze * weight_pat) / (inaccuracy * weight * doze))

    def turn_new_day(day, prev): #переход в новый день
        return day.fromordinal(day.toordinal() + prev + 3)
    def turn_new_day1(day, n): #переход в новый день
        return day.fromordinal(day.toordinal() + prev + 4)
    def turn_new_day2(day, n): #переход в новый день
        return day.fromordinal(day.toordinal() + prev + 5)

    dict_for_json = {} #словарь из день - день недели - человеки
    dict_for_json_w = {} #словарь из день - день недели - вес

    count = 0
    prev = 0
    for n in range(150):
        day_of_week = turn_new_day(day_of_load, prev).weekday()
        if count == 150:
            if day_of_week == 5:
                prev += 2
            elif day_of_week == 6:
                prev += 1
            day_of_load = day_of_load.fromordinal(day_of_load.toordinal() + prev - 1)
            count = 0
            prev = 0
        day_of_period = count
        if day_of_week == 5: #если суббота
            day_of_week = turn_new_day2(day_of_load, prev).weekday()
            day_n = str(turn_new_day2(day_of_load, prev))
            people = opportunity_people(average_weight, day_of_period, inaccuracy, doze, weight[day_n])
            dict_for_json[str(turn_new_day2(day_of_load, prev))] = people
            dict_for_json_w[str(turn_new_day2(day_of_load, prev))] = math.floor(-(weight[day_n]) + (Gbq[day_of_period // 3] / (inaccuracy * doze)))
            prev += 5
        elif day_of_week == 6: #если воскресение
            day_of_week = turn_new_day1(day_of_load, prev).weekday()
            day_n = str(turn_new_day1(day_of_load, prev))
            people = opportunity_people(average_weight, day_of_period, inaccuracy, doze, weight[day_n])
            dict_for_json[str(turn_new_day1(day_of_load, prev))] = people
            dict_for_json_w[str(turn_new_day1(day_of_load, prev))] = math.floor(-(weight[day_n]) + (Gbq[day_of_period // 3] / (inaccuracy * doze)))
            prev += 4
        else:
            day_n = str(turn_new_day(day_of_load, prev))
            people = opportunity_people(average_weight, day_of_period, inaccuracy, doze, weight[day_n])
            dict_for_json[str(turn_new_day(day_of_load, prev))] = people
            dict_for_json_w[str(turn_new_day(day_of_load, prev))] = math.floor(-(weight[day_n]) + (Gbq[day_of_period // 3] / (inaccuracy * doze)))
            prev += 3
        count += 3


    json_str = json.dumps(dict_for_json, skipkeys = True, ensure_ascii = True, #строка json
               check_circular = False, allow_nan = False, cls = None, indent = None,
               separators = None, default = None, sort_keys = True)

    outp = open('json.txt', 'w')
    outp.write(json_str)
    outp.close()

    json_str = "var st = " + json_str
    outp = open('quant/quant.json', 'w')
    outp.write(json_str)
    outp.close()

    json_str_w = json.dumps(dict_for_json_w)
    json_str_w = "var st_w = " + json_str_w
    outp = open('weight/weight.json', 'w')
    outp.write(json_str_w)
    outp.close()

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


elif wall.adminust(user):

    inp = codecs.open('fill/fill.json', 'r')
    text = inp.read()
    fills = json.loads(text)
    inp.close()


    pub1 = '''
<!DOCTYPE HTML>
<html>
<head>
<meta charset="utf-8">
<title>Загрузки</title>
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
    <style>
    .button {
        position: relative;
	    background: white;
	    border: 2px solid #c2e1f5;
    }
    </style>
    '''
    print(pub)
    print('<form align ="left" action="/cgi-bin/fillings.py">')
    print('Генератор1:<input type="text" name="ndate" value = {}>'.format(fills[0]))
    print('<input type="hidden" name="action" value="change">')
    print('<input class ="button" type="submit" value="Изменить">')
    print('</form>')

    print('</body>')
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
