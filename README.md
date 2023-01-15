# Python

**Python** - это легкочитаемый, высокоуровневый, интерпретируемы язык программирования с сильной динамической типизацией, который поддерживает принципы ООП.

- *легкочитаемый* - сообщество соблюдает соглашения о форматировании (PEP8),
- *высокоуровневый* - язык близок к человеческому языку,
- *интерпретируемый* - интерпретатор исполняет команды непосредственно, а не компилирует их в машинный код,
- *строгая типизация* - отсутствуют неявные преобразования типов, например: нельзя сложить строку с числом,
- *динамическая типизация* - тип переменных определяется в момент их инициализации и может изменяться в зависимости от значения,
- *ООП* - подразумевают инкапсуляцию кода в особые структуры, именуемые объектами.


## Переменные

**Переменная** - это имя связанное с объектом в памяти компьютера. Все в python является объектом. \
**объект** - экземпляр класса, который имеет атрибуты и методы. \
**Структура данных** - это метод организации набора данных, оптимизированный под конкретную задачу.

Объекты делятся на неизменяемые (immutable) и изменяемые (mutable), еще есть **None**. 
Неизменяемый тип данных означает, что изменение значения приведет к созданию нового объекта.


## Неизменяемые объекты

1) ### Числовые

- #### int (целые числа)

```python
a = 5
print(type(a))  # <class 'int'>
print(hex(id(a)))  # место хранения в памяти (его использует оператор is)
print(int.__doc__)  # посмотреть документацию
dir(int)  # посмотреть атрибуты и методы
```

- #### complex (комплексные числа)

```python
x = 52 + 4j
print(x.real, x.imag)  # 52.0 4.0
```

- #### float (числа с плавающей запятой)

```python
a = 3.4
a.is_integer()  # False
```

2) ### bool (логические значения)

```python
# False / True  # 0.0
print(bool.__bases__)  # (<class 'int'>,)
```

3) ### str (строки)

> последовательность символов в кодировке Unicode

```python
s = '-'.join("ab.abA ".strip().split('.'))
# s = "ab-abA"
print(s.partition('-'))  # ('ab', '-', 'abA')  # три части
print(s.startswith('ab'))  # True

print(s.capitalize())  # Ab-aba
print(s.upper())  # AB-ABA
print(s.lower())  # ab-aba

print(s.count('a'))  # 2
print(s.find('a'))  # 0  # rfind - с конца
print(s.replace('a', 'c'))  # cb-cbA
```

> [&#x1f352;](https://unicode-table.com/ru/)

```python
heart_symbol = chr(0x2665)  # '♥'
unicode_code = hex(ord('♥'))  # 0x2665

with open("text.txt", "w", encoding="utf-16", errors='ignore') as f:  # ascii, cp1251
    f.write(heart_symbol)
```

- bytes (бинарные данные)

```python
b = b"text"  # ascii
b = b"\x01\x02\x03\x04"
```

4) ### tuple (кортежи)

> неизменяемые списки

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

- #### frozenset (неизменяемые множества)

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
l.extend([4, 5])
print(l.pop())  # удаление с конца
l.remove('Daniil')

for ind, val in enumerate(l):
    pass
```

> **List Comprehensions** - способ создать список на основе последовательности.

```python
squares = [i**2 for i in range(1, 11) if i % 2 == 0]  # [4, 16, 36, 64, 100]
```

- #### array (массивы)

> Массивы хранят элементы одного и того же типа

```python
import array
a = array.array('i', [1, 2, 3, 4]) 
```

- #### deque (очереди)

> двусвязный список

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

```python
s = {1, 2, 3}
s.add(4)
s.update((5, 6))
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

> хэш-таблица - неупорядоченный набор пар ключ / значение (ключи — уникальные хэшируемые объекты)

```python
A = {'name': 'Daniil', 'age': 26}
A['height']  # KeyError
A.get('height', 176)

A.update({'s': 'sa'})
print(A.pop('s'))  # 'sa'

for key, val in A.items():
    pass
```

- #### OrderedDict (упорядоченный словарь)

```python
from collections import OrderedDict

A = OrderedDict({'name': 'Daniil', 'age': 26})
print(A.popitem(last=True))  # ('age', 26)
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
