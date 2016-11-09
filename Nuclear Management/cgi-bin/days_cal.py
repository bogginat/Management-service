import datetime
import math
import json, codecs

inp = codecs.open('json.txt', 'r')
text = inp.read()
data = json.loads(text)
inp.close()

weight = {}

keys = list(data.keys())
print(keys)

for elem in keys:
    weight[elem] = 0;

inp = codecs.open('patients.txt', 'r')
text = inp.read()
patients = json.loads(text)
inp.close()

for elem in patients:
    s = elem[0]
    weight[s] += int(elem[4]);


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