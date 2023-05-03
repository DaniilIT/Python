# Работа с датой и временем

получить текущую точку:

```python
import datetime as dt

dt_now = dt.datetime.now()  # 2023-04-26 10:18:51.943884  # <class 'datetime.datetime'>
# current_date = dt_now.date()
current_date = dt.date.today()  # 2023-04-26  # <class 'datetime.date'>
# current_time = dt_now.time()
current_time = dt_now.time()  # 10:18:51.943884  # <class 'datetime.time'>
```

создать точку:

```python
# year, month, day, hour, minute, second, microsecond
dt_obj = dt.datetime(2023,04,26,8,48,45)  # 2023-04-26 08:48:45
date_obj = dt.date(2023,04,26)  # 2023-04-26
timeobj = dt.time(8,48,45)  # 08:48:45

dt_point = dt.datetime.strptime('2023-04-26 08:48:45', '%Y-%m-%d %H:%M:%S')
print(dt_now.strftime('%m/%d/%y %H:%M:%S'))  # 04/26/23 12:13:14
print(dt_now.timestamp())  # 1682500394.136089  # эпоха с 1970 UTC
dt_now = dt.datetime.fromtimestamp(1682500394)
```

|**Символ**|**Описание**|**Пример**|
|:---:|:---:|:---:|
|%a|День недели, короткий вариант|Wed|
|%A|День недели, полный вариант|Wednesday|
|%w|День недели числом, 0 – воскресенье|3|
|%d|День месяца|31|
|%b|Название месяца, короткий вариант|Dec|
|%B|Название месяца, полный вариант|December|
|%m|Месяц числом|12|
|%y|Год, короткий вариант|18|
|%Y|Год, полный вариант|2018|
|%H|Час, 24|17|
|%h|Час, 12|05|
|%p|AM/PM||
|%M|Минута|41|
|%S|Секунда|08|

разница:

```python
td_object =dt.timedelta(days=1, seconds=0, minutes=0, hours=0)  # 1 day, 0:00:00 <class 'datetime.timedelta'>
time_diff = dt.date(2022, 10, 30) - dt.date(2022, 10, 2)
print(time_diff.days)  # 26
print(time_diff.total_seconds())  # 2419200
```

## Часовые пояса

```sh
python -m pip install pytz
```

```python
import pytz
from datetime import timezone as tz

dt_now = dt.datetime.utcnow()  # 2023-04-26 08:35:06.271916
dt_utc_now = pytz.utc.localize(dt_now)  # 2023-04-26 08:35:06.271916+00:00
dt_utc_now = dt.datetime.now(tz=tz.utc)  # 2023-04-26 08:35:06.271916+00:00
dt_now = dt.datetime.now(tz=pytz.utc)  # 2023-04-26 08:35:06.271916+00:00

print(pytz.all_timezones)  # ['America/New_York', 'Etc/GMT+3', 'Europe/Moscow', ...]
print(pytz.country_timezones('RU'))  # ['Europe/Moscow', ...]

tz_moscow = pytz.timezone("Europe/Moscow")
dt_moscow =dt.datetime.now(tz_moscow)  # 2023-04-26 11:19:37.507613+03:00 <class 'datetime.datetime'>
print(dt_moscow.tzinfo)  # Europe/Moscow  # возможно None

tz_newyork = pytz.timezone('America/New_York')
dt_newyork = tz_newyork.localize(dt_now)  # 2023-04-26 11:26:04.425242-04:00 <class 'datetime.datetime'>
```

## time

```python
from time import sleep

time.time()  # == dt.datetime.now().timestamp()

start = time.monotonic()
time.sleep(1)  # пауза 1с.
print(f'Program time: {time.monotonic() - start:.3f}' + " seconds.")
```

Измерить время выполнения скрипта:

```sh
time main.py
```


## te quiero demasiado

```python
from tqdm import tqdm
for i in tqdm(range(n)):
    ...
```
