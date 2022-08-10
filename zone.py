from datetime import datetime
import pytz

zones = pytz.all_timezones
print(len(zones))
print(zones[577:]) 
print("Enter the number beside your local time zone:")
num = 1
us_zones = zones[577: 588]
for zone in us_zones:
    print(str(num) + " " + zone)
    num += 1

timezone_num = input("choice: ")
timezone = us_zones[int(timezone_num) - 1]
print(timezone)
local_time = pytz.timezone(timezone) 
today = datetime.now(local_time)