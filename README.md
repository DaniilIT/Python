# Python

**Python** - это легкочитаемый, высокоуровневый, интерпретируемы язык программирования с сильной динамической типизацией, который поддерживает принципы ООП.

- *легкочитаемый* - сообщество соблюдает соглашения о форматировании (PEP8),
- *высокоуровневый* - язык близок к человеческому языку,
- *интерпретируемый* - интерпретатор исполняет команды непосредственно, а не компилирует их в машинный код,
- *строгая типизация* - отсутствуют неявные преобразования типов, например: нельзя сложить строку с числом,
- *динамическая типизация* - тип переменных определяется в момент их инициализации и может изменяться в зависимости от значения,
- *ООП* - подразумевают инкапсуляцию кода в особые структуры, именуемые объектами.

[Пособие по Python](https://docs.python.org/3/tutorial/)

## Переменные

**Переменная** - это название для зарезервированного места в памяти компьютера.\
Всё в python является объектом. \
**Объект** - это экземпляр класса, который имеет атрибуты и методы. \
**Структура данных** - это метод организации набора данных, оптимизированный под конкретную задачу.

Объекты делятся на неизменяемые (*immutable*) и изменяемые (*mutable*). 
Неизменяемый тип данных означает, что изменение значения приведет к созданию нового объекта.


## Неизменяемые объекты

1) ### NoneType

> `None` указывает на отсутствие значения

2) ### Числовые

- #### int (целые числа)

```python
num = 5
print(type(num))  # <class 'int'>
print(hex(id(num)))  # место хранения в памяти (его использует оператор is)
int('0x2A', base=16)  # 42  # bin(42) => '0b101010'
print(int.__doc__)  # посмотреть документацию
dir(int)  # посмотреть атрибуты и методы
```

- #### float (числа с плавающей запятой)

```python
pi = 3.14
pi.is_integer()  # False

from math import ceil, floor, trunc
round(pi, 2)  # округление до ближайшего или четного
ceil(pi), floor(pi)  # округление вправо и влево соответственно
int(pi), trunc(pi)  # округление в сторону 0
```

- #### complex (комплексные числа)

```python
x = 3 + 4j
print(x.real, x.imag)  # 3.0 4.0
```

3) ### bool (логические значения)

> `True` и `False`

```python
print(bool.__bases__)  # (<class 'int'>,)
res_0 = True and ' ' and [''] and 0 and 1  # 0 - первое ложное или последнее
res_1 = False or None or '' or [] or 1 or 0  # 1 - первое истинное или последнее
```

4) ### str (строки)

> Последовательность символов в кодировке *Unicode*

```python
s = '-'.join('ab.abA '.strip().split('.'))
# s = 'ab-abA'
print(s.partition('-'))  # ('ab', '-', 'abA')  # три части
print(s.startswith('ab'))  # True

print(s.ljust(8, '-'))  # 'ab-abA--'
print(s.capitalize(), s.title())  # Ab-aba Ab-Aba
print(s.upper(), s.lower())  # AB-ABA ab-aba
print(s.casefold()=='ab-aba')  # True - безрегистровое сравнение

print(s.count('a'))  # 2
print(s.find('a'))  # 0  # возможно -1  # rfind - с конца
print(s.index('a'))  # 0  # возможно ValueError  # rindex - с конца
print(s.replace('a', 'c'))  # cb-cbA
```

> `&#x1f352;` [&#x1f352;](https://unicode-table.com/ru/)
о́
```python
cherries_name = print('🍒'.encode('ascii', 'namereplace'))  # b'\\N{CHERRIES}'
print('\N{CHERRIES}')  # '🍒'

print(f'0b{ord("♥"):016b}')  # 0b0010011001100101
heart_unicode = hex(ord('♥'))  # 0x2665
heart_symbol = chr(0x2665)  # '♥'

with open('text.txt', 'w', encoding='utf-16') as f:  # ascii, cp1251
    f.write(heart_symbol)
```

#### Форматирование строк

```python
name, number, code = 'Daniil', 3.14159, 42

# оператор %
print('%-8s|%05.2f|0x%x' % (name, number, code))  # 'Daniil  |03.14|0x2a'

# метод format
print('{name:8s}|{number:05.2f}|{code:#x}'.format(name=name, number=number, code=code))
print('{:8s}|{:05.2f}|{:#x}'.format(name, number, code))
print('{2:8s}|{1:05.2f}|{0:#x}'.format(code, number, name))

# f-строки
print(f'{name:<8s}|{number:05.2f}|{code:#x}')

# шаблоны (нет доступа к произвольным переменным)
from string import Template
t = Template('${name}|${number}|${code}')
print(t.substitute(name=name, number=number, code=code))
```

- bytes (бинарные данные)

```python
b = b'text'  # ascii
b = b'\x01\x02\x03\x04'
```

5) ### tuple (кортежи)

> неизменяемые списки

Кортежи обычно используются для хранения и передачи неизменяемых данных,
например, координаты точки на плоскости.

```python
t = (1, 'Daniil')
t.count(1)  # 1
```

- #### namedtuple (именованные кортежи)

```python
from collections import namedtuple

Person = namedtuple('Person', ('name', 'age'))
nt = Person('Daniil', 26)
nt.name == nt[0]
```

6) ### frozenset

> неизменяемые множества

```python
fs = frozenset({1, 'Daniil'})
hash(fs)

fs = frozenset({[1, 2], 'Daniil'})
hash(fs)  # TypeError
```


## Изменяемые объекты

1) ### list (списки)

> упорядоченная (индексированная) коллекция

```python
l = [1, 2, 'Daniil']
l.append(3)  # добавление в конец
l.extend([4, 5])  # добавление нескольких элементов
l.insert(2, 'el')  # вставка
print(l.pop())  # удаление с конца, возможно IndexError
l.remove('Daniil')  # возможно ValueError

l.sort(reverse=True)  # на месте
# Отсортировать список, в котором есть и числа и строки, через функцию
l = sorted(l, key = lambda x: (isinstance(x, str), x))

for idx, value in enumerate(l):
    print(idx, value)
```

> **List Comprehensions** - способ создать список на основе последовательности.

```python
squares = [i**2 for i in range(1, 11) if i % 2 == 0]  # [4, 16, 36, 64, 100]
```

- #### array (массивы)

> Массивы хранят элементы одного и того же типа

```python
import array as arr
a = arr.array('i', [1, 2, 3, 4]) 
```

- #### deque (очереди)

> двусвязный список

list - LIFO (стек), deque - FIFO.

```python
from collections import deque

q = deque([1, 2, 'Daniil'])
q.appendleft(0)
print(q.popleft())
```

- #### bytearrays (байтовые массивы)

> элементы < 256

```python
a = bytearray([12, 8, 25])
```

2) ### set (множества)

> неупорядоченная коллекция уникальных хэшируемых элементов

Множества предпочтительно использовать для решения задач, связанных с уникальностью элементов,
например, удаление дубликатов из списка, проверка пересечения элементов в нескольких списках и т.д.

```python
s = {1, 2, 3}
s.add(4)
s.update((5, 6))
s.remove(5)  # возможно KeyError
s.discard(6)  # удалит, если есть
```
```python
a = {1, 2, 3, 4}
b = {3, 4, 5}
print(a.difference(b))  # a - b  # {1, 2}
print(a.symmetric_difference(b))  # a ^ b  # {1, 2, 5}
print(a.intersection(b))  # a & b  # {3, 4}
print(a.union(b))  # a | b  # {1, 2, 3, 4, 5}
```
```python
a = {1, 2, 3, 4}
b = {3, 4}
print(b.issubset(a))  # True
print(a.issuperset(b))  # True
```

3) ### dict (словари)

> подобная хэш-таблице структура - неупорядоченный набор пар ключ / значение (ключи — уникальные хэшируемые объекты)

```python
d = {'name': 'Daniil', 'age': 26}
d['height']  # KeyError
d.get('height', 176)

d.update([('weight', 70)])
del d['weight']  # возможно KeyError
print(d.pop('weight'))  # 70  # возможно KeyError

for key, value in d.items():  # keys(), values()
    print(key, value)
```

- #### OrderedDict (упорядоченный словарь)

```python
from collections import OrderedDict

od = OrderedDict({'name': 'Daniil', 'age': 26})
print(od.popitem(last=True))  # ('age', 26)
```

- #### ChainMap (объединенный словарь)

```python
from collections import ChainMap

d1 = {'A': 1, 'B': 2}
d2 = {'B': 3, 'C': 4}
d = ChainMap(d1, d2)
print(d['B'])  # 2
```

- #### defaultdict (словарь со значением по умолчанию)

```python
s = [('A', 1), ('B', 2), ('A', 3)]

d = {}
for k, v in s:
    d.setdefault(k, []).append(v)

# d = {'A': [1, 3], 'B': [2]}    
    
from collections import defaultdict

d = defaultdict(list)
for k, v in s:
    d[k].append(v)
```

- #### Counter (счетчик)

```python
from collections import Counter

c = Counter(['A', 'A', 'B', 'A'])  # {'A': 3, 'B': 1}
c = Counter('AABA')  # {'A': 3, 'B': 1}
```
