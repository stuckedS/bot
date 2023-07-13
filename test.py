import datetime

date = str(datetime.date.today())
print(date)
date = date[8]+date[9]+'/'+date[5]+date[6]+'/'+date[0]+date[1]+date[2]+date[3]
print (date)