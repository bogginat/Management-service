#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cgi
import http.cookies
import os
import json, codecs, datetime

from _wall import Wall
wall = Wall()

cookie = http.cookies.SimpleCookie(os.environ.get("HTTP_COOKIE"))
session = cookie.get("session")
if session is not None:
    session = session.value
user = wall.find_cookie(session)  # Ищем пользователя по переданной куке

form = cgi.FieldStorage()
action = form.getfirst("action", "")

if action == "login": #пытаемся войти
    login = form.getfirst("login", "")
    password = form.getfirst("password", "")
    if wall.find(login, password):
        cookie = wall.set_cookie(login)
        print('Set-cookie: session={}'.format(cookie))
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
    else: #нет такого пользователя(не совпали пароль и логин)
        user = None
        #wall.register(login, password)
        #cookie = wall.set_cookie(login)
        #print('Set-cookie: session={}'.format(cookie))

if action == "logout": #хотим выйти
    now_ses = form.getfirst("text", "")
    tmp = wall.del_cookie(now_ses)
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

if action == "reg": #если хотим зарегистрироваться
    login = form.getfirst("login", "")
    password = form.getfirst("password", "")
    fam = form.getfirst("fam", "")
    im = form.getfirst("im", "")
    otch = form.getfirst("otch", "")
    job = form.getfirst("job", "")
    adm = form.getfirst("adm", "")
    possib = wall.register(login, password, adm)

    if not possib:
        pattern = '''
<!DOCTYPE HTML>
<html>
<head>
<meta charset="utf-8">
  <meta http-equiv="refresh" content="0; url="http:/loginex/loginex.html" />
  <script type="text/javascript"> window.location.href = "http:/loginex/loginex.html" </script>
</head>
</html>
'''
        print(pattern)
    else:
        wall.register1(login, fam, im, otch, job)

year_need = datetime.datetime.now().isoformat().split("-")[0]

if action == "calend":
    year_need = form.getfirst("text", "")

if action == "next":
    year_need = str(int(form.getfirst("text", "")) + 1)

if action == "prev":
    year_need = str(int(form.getfirst("text", "")) - 1)

if user is not None:
    #inp = codecs.open('index.html', 'r', encoding='utf-8')
    #text1 = inp.read().encode('utf-8')
    #inp.close()
    #pub = '''
    #<form action="/cgi-bin/wall.py">
        #<textarea name="text"></textarea>
        #<input type="hidden" name="action" value="publish">
        #<input type="submit">
    #</form>
    #'''
    pub = '''
<!DOCTYPE HTML>
<html>
<head>
<meta charset="utf-8">
<title>Календарь</title>
  <link type="text/css" rel="stylesheet" href="/stylesheets/main.css" />
  <script src="/quant/quant.json" type="text/javascript"></script>
  <script src="/patients/patients.json" type="text/javascript"></script>
  <script src="/weight/weight.json" type="text/javascript"></script>
</head>
<body onload="displayAll()">
    '''
    print('Content-type: text/html\n')
    print(pub)
    print('Пользователь:{}'.format(user))
    print('<form align ="left" action="/cgi-bin/wall.py">')
    print('Год:<input type="text" name="text" value = {}>'.format(year_need))
    print('<input type="hidden" name="action" value="calend">')
    print('<input type="submit" class ="button" value="Переход"><br>')
    print('</form>')
    print('<form align ="right" action="/cgi-bin/wall.py">')
    print('<input type="text" name="text" class ="area_logout" value = {}>'.format(session))
    print('<input type="hidden" name="action" value="logout">')
    print('<input class ="button" type="submit" value="Выйти">')
    print('</form>')
    if wall.adminust(user):
        print('<form align ="right" action="/cgi-bin/registrate.py">')
        print('<input type="hidden" name="action" value="reg">')
        print('<input type="submit" class ="button" value="Управление пользователями">')
        print('</form>')
        print('<form align ="right" action="/cgi-bin/fillings.py">')
        print('<input type="submit" class ="button" value="Управление загрузками">')
        print('</form>')
    sub4 = '''
<form align="left" action="/cgi-bin/patients_find.py" method="get" name = "form_f" class = "forma_f" id = "format_f">
        Фамилия пациента:
        <input type="text" name="firstname_f">
        <input class ="button" type="submit" value="Найти">
    </form>'''
    print(sub4)
    print('<form align ="center" action="/cgi-bin/wall.py">')
    print('<input type="text" name="text" class ="area_logout" value = {}>'.format(year_need))
    print('<input type="hidden" name="action" value="prev">')
    print('<button type="submit" class="arrow_box1" value="Предыдущий год">Предыдущий год</button>')
    print('</form>')
    print('<form align ="center" action="/cgi-bin/wall.py">')
    print('<input type="text" name="text" class ="area_logout" value = {}>'.format(year_need))
    print('<input type="hidden" name="action" value="next">')
    print('<button type="submit" class="arrow_box" value="Следующий год">Следующий год</button>')
    print('</form>')
    sub = '''
    <style>
  </style>
<p>    </p>
<table  align="left" border="3" cellspacing="0" bordercolor="#810B2E" width="80%" hight="50%">
  <tr>
    <td valign="top"><div id="calendar0"></div></td>
    <td valign="top"><div id="calendar1"></div></td>
    <td valign="top"><div id="calendar2"></div></td>
    <td valign="top"><div id="calendar3"></div></td>
  </tr>
  <tr>
    <td valign="top"><div id="calendar4"></div></td>
    <td valign="top"><div id="calendar5"></div></td>
    <td valign="top"><div id="calendar6"></div></td>
    <td valign="top"><div id="calendar7"></div></td>
  </tr>
  <tr>
    <td valign="top"><div id="calendar8"></div></td>
    <td valign="top"><div id="calendar9"></div></td>
    <td valign="top"><div id="calendar10"></div></td>
    <td valign="top"><div id="calendar11"></div></td>
  </tr>
</table>
   <hr>
<p id="data" class="datatext"></p>
<p id="place"></p>
<p id="patient"></p>
<p id="patient_w"></p>
<div id="b"></div>
<p id="no"></p>
<form align="right" action="/cgi-bin/pat_on_date.py" method="get" id = "data_on_date" class="date_on1">
      <input name="guestbook_name" id = "date_on_2"><input type="submit" value="">
    </form>
<hr>
    <form align = "right" action="/cgi-bin/pati.py" method="get" name = "form" class = "forma" id = "format">
        Дата:<br>
        <input type="text" name="date" id="date">
        <br>
        Имя:<br>
        <input type="text" name="firstname">
        <br>
        Фамилия:<br>
        <input type="text" name="surname">
        <br>
        Отчество:<br>
        <input type="text" name="lastname">
        <br>
        Вес:<br>
        <input type="text" name="w">
        <br>
      <div><input type="submit" value="Записать"></div>
    </form>
    <hr>
<form id = "date_on1" class = "date_on1">Данные по дате:
      <input name="guestbook_name" id = "date_on">
      <button id = "button_data">Перезагрузить</button>
    </form>
<style>

.datatext {
 font-size: 30px;
}

.forma {
 visibility: hidden;
}
.list {
visibility: visible;
}
</style>

<script>
function displayCalendar(mon){


 var htmlContent ="";
 var FebNumberOfDays ="";
 var counter = 1;


 var dateNow = new Date();
 var month = mon;

 var nextMonth = month+1; //+1; //Used to match up the current month with the correct start date.
 var prevMonth = month -1;
 var day = dateNow.getDate(); //целое число от 1 до 31
 '''
    print(sub)
    print("var year = {}".format(year_need))
    us = '''
 //Determing if February (28,or 29)
 if (month == 1){
    if ( (year%100!=0) && (year%4==0) || (year%400==0)){
      FebNumberOfDays = 29;
    }else{
      FebNumberOfDays = 28;
    }
 }


 // names of months and week days.
 var monthNames = ["Январь","Февраль","Март","Апрель","Май","Июнь","Июль","Август","Сентябрь","Октябрь","Ноябрь", "Декабрь"];
 var dayNames = ["Monday","Tuesday","Wednesday","Thrusday","Friday", "Saturday", "Sunday"];
 var dayPerMonth = ["31", ""+FebNumberOfDays+"","31","30","31","30","31","31","30","31","30","31"]


 // days in previous month and next one , and day of week.
 var nextDate = new Date(nextMonth+' 1 ,'+year);
 var weekdays= nextDate.getDay();
 if (weekdays == 0) {
    weekdays = 7;
 }
 var weekdays2 = weekdays;
 var numOfDays = dayPerMonth[month];




 // this leave a white space for days of pervious month.
 while (weekdays > 1){
    htmlContent += "<td class='monthPre'></td>";

 // used in next loop.
     weekdays--;
 }

 // loop to build the calander body.
 while (counter <= numOfDays){

     // When to start new line.
    if (weekdays2 > 7){
        weekdays2 = 1;
        htmlContent += "</tr><tr>";
    }
    //МОЙ КОД
    var my_day = counter.toString();
    if (counter < 10) {
        my_day = '0' + my_day;
    }
    month_n = mon + 1;
    if (month_n < 10) {
        var my_month = month_n.toString();
        my_month = '0' + my_month;
    } else {
        var my_month = month_n;
    }
    var my_year = year.toString();
    var date = my_year+'-'+my_month+'-'+my_day;

    if (date in st) {
        if(st[date] == 0) {
            htmlContent +="<td class='day0'>"+counter;
        } else if(st[date] == 1) {
            htmlContent +="<td class='day1'>"+counter;
        } else if(st[date] > 1) {
            htmlContent +="<td class='day2'>"+counter;
        }
        htmlContent += " <small><small>(" + st[date] + ")</small></small></td>"
    } else {
        htmlContent +="<td class='monthNow'>"+counter+"</td>";
    }

    weekdays2++;
    counter++;
 }



 // building the calendar html body.
 var calendarBody = "<table class='calendar' id = 'mon"+mon+"'> <tr class='monthNow'><th colspan='7'>"
 +monthNames[month]+" "+ year +"</th></tr>";
 calendarBody +="<tr class='dayNames'><td>Пн</td> <td>Вт</td>"+
 "<td>Ср</td> <td>Чт</td> <td>Пт</td> <td>Сб</td> <td>Вс</td> </tr>";
 calendarBody += "<tr>";
 calendarBody += htmlContent;
 calendarBody += "</tr></table>";
 // set the content of div .
 document.getElementById("calendar" + mon).innerHTML=calendarBody;
 var table = document.getElementById("mon"+mon+"");
    if (table != null) {
        for (var i = 0; i < table.rows.length; i++) {
            for (var j = 0; j < table.rows[i].cells.length; j++)
            table.rows[i].cells[j].onclick = function () {
                tableText(this);
            };
        }
    }
function tableText(tableCell) {
        document.getElementById("format").style.visibility = "hidden";
        document.getElementById("b").innerHTML = '';
        var day_now = tableCell.innerHTML.split(' ');
        if (Number(day_now[0]) < 10) {
            var my_day = '0' + Number(day_now[0]).toString();
        } else {
            var my_day = Number(day_now[0]).toString();
        }
        month_n = mon + 1;
        if (month_n < 10) {
            var my_month = month_n.toString();
            my_month = '0' + my_month;
        } else {
            var my_month = month_n.toString();
        }
        var my_year = year.toString();
        var date = my_year+'-'+my_month+'-'+my_day;
        document.getElementById("data").innerHTML = date;

        document.getElementById("date_on").value = date;
        document.getElementById("date_on_2").value = date;
        var form = document.getElementById("data_on_date");
        form.submit();
    }

}
function displayAll(){
displayCalendar(0);
displayCalendar(1);
displayCalendar(2);
displayCalendar(3);
displayCalendar(4);
displayCalendar(5);
displayCalendar(6);
displayCalendar(7);
displayCalendar(8);
displayCalendar(9);
displayCalendar(10);
displayCalendar(11);
}
</script>

<script>
var QueryString = function () {
  // This function is anonymous, is executed immediately and
  // the return value is assigned to QueryString!
  var query_string = {};
  var query = window.location.search.substring(1);
  var vars = query.split("=");
  vars = vars[1].split("/");
  return vars[0];
}();

document.getElementById("date_on").value = QueryString;
document.getElementById("date_on_2").value = QueryString;
document.getElementById("date").value = QueryString;

if(QueryString in st && st_w[QueryString] > 0) {
    document.getElementById("patient").innerHTML = "Можно записать: "+st[QueryString]+"(примерно, из рассчета на вес 76кг).";
    document.getElementById("patient_w").innerHTML = "Доступный вес: "+st_w[QueryString]+"кг.";
    document.getElementById("format").style.visibility = "visible";
    document.getElementById("data").innerHTML = QueryString;
} else if (QueryString in st && st_w[QueryString] == 0) {
    document.getElementById("patient").innerHTML = "Полная запись(из рассчета на вес 76кг).";
    document.getElementById("format").style.visibility = "visible";
    document.getElementById("patient_w").innerHTML = "Доступный вес: "+st_w[QueryString]+"кг.";
    document.getElementById("data").innerHTML = QueryString;
} else {
    document.getElementById("patient").innerHTML = "";
}
</script>
<script>
   document.getElementById("but_f").onclick = function() {
        document.getElementById("format_f").style.visibility = "visible";
   };
</script>
</body>
<style>
.monthPre{
 color: grey;
    border: white;
 text-align: center;
 cursor: pointer;
}
.monthNow{
 color: grey;
    border: white;
 text-align: center;
 cursor: pointer;
}
.dayNow{
 border: white;
 color: grey;
 text-align: center;
 cursor: pointer;
}
.calendar td{
 htmlContent: 2px;
 width: 20%;
 height: 20%;
    border: white;
 cursor: pointer;
}
.monthNow th{
 background-color: #A64600;
 color: #FFFFFF;
 text-align: center;
    border: white;
 cursor: pointer;
}
.dayNames{
 background: #810B2E;
 color: #FFFFFF;
 text-align: center;
 cursor: pointer;
}
.day1{
 background: yellow;
 border: white;
 color: grey;
 text-align: center;
 cursor: pointer;
}
.day2{
 background: #62E200;
 border: white;
 color: white;
 text-align: center;
 cursor: pointer;
}
.day0{
 background: #FF1800;
 border: white;
 color: white;
 text-align: center;
 cursor: pointer;
}
    .date_on1{
    visibility: hidden;
    display: none;
    }
    .area_logout{
    visibility: hidden;
    }
</style>
</html>'''
    print(us)
else:
    pub = '''
    <!DOCTYPE HTML>
<html>
<head>
<meta charset="utf-8">
<title>Вход</title>
</head>
<body>
Форма для входа.
    <form action="/cgi-bin/wall.py">
        Логин: <input type="text" name="login"><br>
        Пароль: <input type="password" name="password"><br>
        <input type="hidden" name="action" value="login">
        <input type="submit" class="button" value = "Вход">
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
    print('Content-type: text/html\n')
    print(pub)

