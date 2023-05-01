# Асихронный код

– выполняется в рамках одного потока (процесса), не про многопоточность и не про многопроцессность.

### Задачи

1. Завязаны на работе с CPU/GPU (*выполняются быстро*)
	* вычисления
	* хэширование
	* рендеринг видео/аудио
2. Завязаны на вводе/ввыводе (I/O) (*выполняются медленно*, асихронность решает проблему ожидания.)
	* сеть
	* базы данных
	* диск

Синхронный код – означает, что инструкции выполняются последовательно.\
Все функции являются **блокирующими**, т. к. они блокируют выполнение программы до тех пор пока не закончат свою работу
и не вернут результат (без return возвращают неявно None). Вместе с результатом возвращается **контроль выполнения** программы в то место откуда произошел вызов функции.

### Асихронный код

– позволяет переключиться на выполнение другой задачи как только первая начинает ждать результат.
Достигается это с помощью:
1. Конструкций языка, которые позволяют передавать управление потоком выполнения программой
	* генераторы
	* синтаксис sync / await
2. Событийный цикл

### Событийный цикл

– менеджер, который управлениет задачами, решает какой код должен выполняться в тот или иной момент.

**select** - системная функция, которая мониторит изменение состояний файловых объектов.

- [01_select.py](01_select.py)
- [02_selectors.py](02_selectors.py)

[Round Robin](https://ru.wikipedia.org/wiki/Round-robin_(%D0%B0%D0%BB%D0%B3%D0%BE%D1%80%D0%B8%D1%82%D0%BC)) (Карусель) – алгоритм, который представляет собой перебор задач по круговому циклу.

```python
from collections import deque
from time import time

def gen(n):
	for i in range(n):
		yield i

tasks = deque([gen(2), gen(5)])

while tasks:
    task = tasks.popleft()
    try:
        print(next(task))
        tasks.append(task)
    except StopIteration:
        pass
```

- [03_0_async_gens.py](03_0_async_gens.py)
- [03_async_gens.py](03_async_gens.py)

**Генераторы**

```python
from inspect import getgeneratorstate

def gen(n):
    for i in range(n):
        try:
            message = yield 'response'
            print('Received:', message)
            # if i == 10:
            #     return 'By!'  # бросится StopIteration: By!
        except StopIteration:
            print('By!')

g = gen(2)
getgeneratorstate(g)  # 'GEN_CREATED'
# r = next(g)  # response
r = g.send(None)  # response
getgeneratorstate(g)  # 'GEN_SUSPENDED'
try:
    # r = next(g)  # Received: None # ByBy!
    r = g.send('Hi!')  # Received: Hi! # ByBy!
    print(r)  # response
    g.throw(StopIteration)  # By! # ByBy!
except StopIteration:
    print('ByBy!')
getgeneratorstate(g)  # 'GEN_CLOSED'
```

- [04_moving_average.py](04_moving_average.py)
- [05_yield_from.py](05_yield_from.py)


## Coroutines (Корутины)

– это функции, которые обьявлены с помощью `async def`, могут выполняются только в событийном цикле и которые могут приостанавливать свое действие во время ожидания. Пока корутины "на паузе" может выполняться другой код, что повышает производительность приложений.\
Другими словами, корутины работают точно также как и генераторы, в то же время они могу принимать и возвращать значения как и обычные функции.\
Из корутинов можно вызывать другие корутины и обычные функции, но не наоборот!\

```python
import inspect

def gf():
	yield None
g = gf()
print(
	type(gf),  # <class 'function'>
	inspect.isgeneratorfunction(gf),  # True
	type(g),  # <class 'generator'>
	inspect.isgenerator(g)  # True
)
next(g)  # StopIteration

async def cf():
	return None
c = cf()
print(
	type(cf),  # <class 'function'>
	inspect.iscoroutinefunction(cf),  # True
	type(c),  # <class 'coroutine'>
	inspect.iscoroutine(c)  # True
)
``` 

## AsyncIO

– фреймворк для создания событийных циклов, реализует асихронность (конкурентность), т. е. переключение между выполнениями задач I/O в рамках одного потока.

Выполнить корутину:
```python
import asyncio

async def c():
	await asyncio.sleep(1)

asyncio.run(c())  # событийный цикл
```

run:
1. создает и запускает Event Loop
2. оборачивает coroytine в объект Task, тем самым запланировав её выполнение в событийном цикле
3. ожидает (await), когда задача завершится
4. закрывает Event Loop

**async** – ключевое слово для создания асихронных (корутинновых) функций.

**await** – ключевое слово для вызова корутин внутри других корутин.

```python
async def main():
	await asyncio.sleep(3)  # time.sleep(3)

asyncio.run(main()) 
# корутира main встанет на паузу пока await не завершится
```

- [06_asyncio_async_await.py](06_asyncio_async_await.py)

**Совет**: при чтении кода стараться представить, что в нем нет слов *asyncio*, *async*, *await*, логика при это не потеряется. 

```python
import asyncio

async def func(t):
    await asyncio.sleep(t)
    return 'Ok'
 
async def main():
	# Эти задачи выполнятся последовательно:
    # res1 = func(3)
    # res2 = func(3)
    
    # Эти задачи выполнятся асихронно:
    res1 = asyncio.create_task(func(3))
    res2 = asyncio.create_task(func(3))
    # как только первая задача дойдет до wait, начнет выполняться вторая
    
    print(await res1)  # дожидается выполнения задачи
    print(await res2)  # если не дожидаться, то программа завершится

if __name__ == '__main__':
    asyncio.run(main())
```

чтобы выполнить крутины конкурентно (асихронно), необходимо использовать задачи (tasks):

## Tasks

– обертка над корутиной, которые планируют выполнение этой корутины в событийном цикле, также может отменять корутину, если она выполняется слишком долго.\ 
Выполнение корутин, обернутых в tasks происходит асихронно и их выполнение не блокируется.

проверить статус задачи:

```python
print(asyncio.all_tasks())  # посмотреть текщие задачи
task = asyncio.create_task(func(), name='task_name')

await task
print(task.get_name())  # task_name  # необходимо для задач из групп
print(task.done())  # True  # проверить статус задачи
print(task.cancelled())  # False  # проверить была ли отменена
task.cancel()  # отменить задачу
```

- [07_cancel.py](07_cancel.py)

### aiohttp

```sh
python -m pip install aiohttp
```

```python
import aiohttp

session = aiohttp.ClientSession()
response = await session.get(url)
if response.ok:
    return response
await session.close()
```

- [08_async.py](08_async.py)

### Асихронные контекстовые менеджеры

```python
import aiohttp

class AsyncSession:
    def __init__(self, url):
        self._url = url

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        response = await self.session.get(self._url)
        return response

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.session.close()

async def check(url):
    async with AsyncSession(url) as response:
        html = await response.text()
        return f'{url}: {html[:20]}'
```

### Группы задач

**gather**

```python
async def main():
    urls = [
        'https://youtube.com',
        'https://google.com',
        # 'https://facebook.com',
    ]
    coros = [check(url) for url in urls]
    
    results = await asyncio.gather(
        *coros,
        return_exceptions=True  # ошибки записываются в результат
    )
    # group1 = asyncio.gather(*coros)
    # groups = asyncio.gather(group1, ...)
    # results = await groups  # [...]
```

В python 3.11 на замену gather пришел **TaskGroup**, который может обрабатывать ошибки, но пока что не может отменять задачи.

```python
try:
	async with asyncio.TaskGroup() as tg:
		task1 = tg.create_task(coro)
	
	results = [task1.result, ...]
except* ValueError as e:
	pass
```

### Вывод результатов по готовности корутин

```python
for coro in asyncio.as_completed(coros):
    result = await coro
    print(result)
```

отмена задач при ошибке в группе:

- [09_group_cancelling.py](09_group_cancelling.py)


### Асихронные итераторы

```python
class AIter:
    def __aiter__(self):
        return self
    async def __anext__(self):
        raise StopAsyncIteration

async for item in AIter():
    print(item)

l = [x async for x in AIter()]
```

- [10_async_for.py](10_async_for.py)  (redis)
- [11_async_comprehensions.py](11_async_comprehensions.py)  (faker)


### Асихронные генераторы

в основном используют для создания контекстных менеджеров.

- [12_async_gens_context_managers.py](12_async_gens_context_managers.py)  (redis)


## Queue (очереди)

Команда await работает в интерактивной оболочке, запущенной с помошью `ipython` – это похоже на записную книжку в Jupyter.
Очереди из asyncio не индексируются и их нельзя перебрать.
нельзя обратиться по индексу

```python
queue = asyncio.Queue(maxsize=4)
await queue.put(n)
n = await queue.get()
```

- [13_async_queue.py](13_async_queue.py)
- [14_queue_practical.py](14_queue_practical.py)


### Запустить сихронный код в корутине

```python
from concurrent.futures import ProcessPoolExecutor

def _parse_link(html):
    soup = BeautifulSoup(html, 'lxml')
    return soup.select_one('div#comic>img').get('src')

loop = asyncio.get_running_loop()
with ProcessPoolExecutor() as pool:
	result = await loop.run_in_executor(
		pool, _parse_link, html
	)
```

### Работа с файлами

```sh
python -m pip install aiofiles
```

```python
import aiohttp

async with aiofiles.open(filename, 'wb') as file:
    async for chunk in response.content.iter_chunked(1024):
        await file.write(chunk)
```


## Синохронизация

– определенное упорядочивание.

* `Lock()`
	- (замки) – часть кода используется одной корутиной в определенный момент. Остальные корутины ожидают в очереди.
* `Semaphore()`
	- (семафоры) – часть кода используется конкретным числом корутин в определенный момент. Подходит для ограничения числа запросов к api.
* `Event()`
	- (события) – обеспечить запуск или продолжение работы корутины при получении разрешения от другой корутины. Подходит для систем уведомлений.
* `Condition()`
	- (условия) – (Event() + Lock()) уведомления о том, что како-то ресурс или кусок кода стал доступным для использования.

- [15_0_server.py](15_0_server.py)  (FastAPI)
- [15_1_client.py](15_1_client.py)
- [15_2_client.py](15_2_client.py)
- [16_event_condition.py](16_event_condition.py)
