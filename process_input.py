from datetime import datetime
import sys
from cron import Cron

if len(sys.argv) == 1 or len(sys.argv) > 2:
    exit("Please Drag in a Single File")

print("""1 for single job
2 for daily job""")
single_daily = input("enter: ")

if single_daily not in ["1", "2"]:
    exit("enter valid number")

if single_daily == "1":
    daily = False
    date = input("enter date (dd-mm-yyyy): ")
    try:
        datetime_date = datetime.strptime(date, '%d-%m-%Y')
    except ValueError:
        exit("Please enter valid date")

else:
    datetime_date = False
    daily = True

time = input("enter time (hh:mm): ")
try:
    datetime_time = datetime.strptime(time, '%H:%M')
except ValueError:
    exit("Please enter valid time")

print(datetime_date.date())
print(datetime_time.time())
Cron().insert(str(datetime_date.date()), str(datetime_time.time()), sys.argv[1], daily=daily)

