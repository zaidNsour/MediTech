from datetime import datetime, timedelta

from config import CLOSING_TIME, OPENING_TIME


'''
date= "2024-10-18T15:30:00"
min = date.split("T")[1].split(":")[1]
hour = date.split("T")[1].split(":")[0]

date_object = datetime.fromisoformat(date)
print(datetime.now() > date_object)

print(f"min:{min}")

if not int(min) in range(0,60,5):
  print("error")
else:
  print("fine")
'''


time_slot = timedelta(minutes= 10)

opening_time = datetime.strptime("11:00","%H:%M")
new_time = opening_time + time_slot

opening_time = datetime.strptime(OPENING_TIME,"%H:%M")
closing_time = datetime.strptime(CLOSING_TIME,"%H:%M")

print(opening_time)



