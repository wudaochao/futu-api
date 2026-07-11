from datetime import datetime
import time

print(datetime.now())
print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

print(time.localtime().tm_wday)

print(time.localtime().tm_year)
print(time.localtime().tm_mon)
print(time.localtime().tm_mday)
print(time.localtime().tm_hour)
print(time.localtime().tm_min)
print(time.localtime().tm_sec)