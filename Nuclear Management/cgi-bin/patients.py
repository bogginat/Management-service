#!/usr/bin/python
# -*- coding: utf-8 -*-
# Import modules for CGI handling
import cgi, cgitb
import json, codecs
import datetime
import math

print ("Content-type:text/html; charset=utf-8\n\n")
# Create instance of FieldStorage
# Create instance of FieldStorage
form = cgi.FieldStorage()

# Get data from fields
firstname = form.getvalue('firstname').decode('utf-8')
lastname = form.getvalue('lastname').decode('utf-8')
surname = form.getvalue('surname').decode('utf-8')
date = form.getvalue('date').decode('utf-8')
w = form.getvalue('w').decode('utf-8')

inp = codecs.open('patients.txt', 'r', encoding = 'utf-8')
json_data = json.load(inp)
inp.close()

#нашли день
weight_pat = 0
for elem in json_data:
    s = elem[0]
    if s == date:
        weight_pat = elem[4]

json_data.append([date, firstname, surname, lastname, w])

json_str_1 = json.dumps(json_data, ensure_ascii=False).encode('utf-8')

outp = open('patients.txt', 'w')
outp.write(json_str_1)
outp.close()

outp = open('patients/patients.json', 'w')
json_str = "var pat = " + json_str_1
outp.write(json_str)
outp.close()

inp = codecs.open('json.txt', 'r')
text = inp.read()
data = json.loads(text)
inp.close()

weight = {}

keys = list(data.keys())

for elem in keys:
    weight[elem] = 0

inp = codecs.open('patients.txt', 'r', encoding = 'utf-8')
patients = json.load(inp)
inp.close()

for elem in patients:
    s = elem[0]
    weight[s] += int(elem[4])


week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
day_of_load = datetime.date(2016, 1, 1)#день загрузки
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


def opportunity(weight, day, inaccuracy, doze): #посчитали, реально ли кого-то уколоть
    return Gbq_Ml[day // 3] >= (inaccuracy * weight * doze) / 2

def opportunity_people(weight, day, inaccuracy, doze, weight_pat):#посчитали, скольких мы можем уколоть
    return opportunity(weight, day, inaccuracy, doze) * math.floor((Gbq[day // 3] - inaccuracy * doze * weight_pat) / (inaccuracy * weight * doze))

def turn_new_day(day, prev): #переход в новый день
    return day.fromordinal(day.toordinal() + prev + 3)
def turn_new_day1(day, n): #переход в новый день
    return day.fromordinal(day.toordinal() + prev + 4)
def turn_new_day2(day, n): #переход в новый день
    return day.fromordinal(day.toordinal() + prev + 5)

dict_for_json = {} #словарь из день - день недели - человеки
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
        prev += 5
    elif day_of_week == 6: #если воскресение
        day_of_week = turn_new_day1(day_of_load, prev).weekday()
        day_n = str(turn_new_day1(day_of_load, prev))
        people = opportunity_people(average_weight, day_of_period, inaccuracy, doze, weight[day_n])
        dict_for_json[str(turn_new_day1(day_of_load, prev))] = people
        prev += 4
    else:
        day_n = str(turn_new_day(day_of_load, prev))
        people = opportunity_people(average_weight, day_of_period, inaccuracy, doze, weight[day_n])
        dict_for_json[str(turn_new_day(day_of_load, prev))] = people
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

print ("<html>")
print ("<head>")
print ("<title>Find</title>")
print ('<meta http-equiv="refresh" content="0; url="http:/index.html" />')
print ('<script type="text/javascript"> window.location.href = "http:/index.html" </script>')
print ("</head>")
print ("<body bgcolor = #A8EEF5>")
print ("</body>")
print ("</html>")
