import datetime
import math
import json, codecs

day = datetime.date(2016, 1, 1)
prev = 0

data = []
for n in range(3000):
    now = day.fromordinal(day.toordinal() + prev)
    data.append(str(now))
    prev+=1


json = json.dumps(data)
outp = open('times.txt', 'w')
outp.write(json)
outp.close()
