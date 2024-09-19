## PEP8

– python enhanced proposal – это руководство по написанию кода на языке Python,
которое содержит стандарты оформления кода для удобства чтения и поддержки проектов.

* имена должны быть понятными и описательными, состоящие из букв, цифр и подчеркивания (snake_case)
* отступы должны быть 4 пробелами, а не табуляцией
* между функциями две пустые строки

Flake8 - линтер

```shell
python -m pip install flake8
python -m flake8
```

## SOLID

– Пять основных принципов проектирования в ООП, которые помогают создавать гибкие, масштабируемые и легко поддерживаемые программы:

* Single Responsibility Principle \
    Принцип единственной ответственности (Класс должен быть ответственным только за одну конкретную задачу)
    - борьба со сложностью
* Open/Closed Principle \
    Принцип открытости/закрытости (Класс должен быть открытым для расширения и закрытым для изменения)
    - главное не сломать код при внесении изменений в программу
* Liskov Substitution Principle \
    Принцип подстановки (на подтипы) (Методы должны быть с ожидаемым поведением)\
    - Подклассы должны дополнять, а не замещать поведение базового класса.
* Interface Segregation Principle \
    Принцип разделения интерфейса (Лучше несколько специфичных классов, нежели один огромный)\
    - Клиенты не должны зависеть от методов, которые они не используют.
* Dependency Inversion Principle \
    Принцип инверсии зависимостей (Высокоуровневые модули не должны зависеть от низкоуровневых модулей (Поля классов должны устанавливаться через конструктор))\
    - убрать зависимость класса бизнес-логики от конкретного низкоуровневого класса, заменив её «мягкой» зависимостью от интерфейса.

### KISS

Keep It Simple, Stupid – избегайте излишней сложности.

### DRY

Don't Repeat Yourself –  избегайте дублирования кода.

### YAGNI

You Aren't Gonna Need It – Избегайте кода "на потом".


## Smell code

– плохо струтурированный код, который и не вызывает ошибок, но который сложен в поддержке.

* дублирование кода
* длиные методы (>10 строк)
* комментарии (код должен быть самодокументированным)
* несоблюдение storage полей (без гетеров и сеттеров)

## Патерны

1. **пораждающие** - отвечают за создание новых объектов.
2. **поведенческие** - отвечают за эффективное и безопасное взаимодействие между объектами.
3. **структурированные** - отвечают за композицию объектов.

### Синглтон

Одиночка – гарантирует, что в программе будет только один экземпляр класса, независимо от того, сколько раз вызовется конструктор.\
Используется для кеш-систем.

```python
class Singleton:
    _instances = None
    
    def __call__(cls, *args, **kwargs):
        if not cls._instances:
            cls._instances[cls] = object.__call__(*args, **kwargs)
        return cls._instances
```

### Фабрика

```python
class A:
    def m(self):
        pass
        
class B:
    def m(self):
        pass

class Factory:
    def __init__(self, factory):
        self.factory = factory
    
    def m(self):
        return self.factory.m()
```

**Антипатерны** – устойчивые грабли, на которые наступило множество программистов.

* программирование копипастом

**Рефакторинг** – процесс исправления ошибок или устранения узких мест в коде.


## [Регулярные выражения](https://cheatography.com/davechild/cheat-sheets/regular-expressions/)

[Подбор](https://regex101.com/)

`[abc]` - `(a|b|c)` | `[^abc]` - ни a, ни b, ни c\
`[6-9]` - `(6|7|8|9)`\
`a{2}` - aa | `a{1,3}` - или a, или aa, или aaa\
`a?` - `a{,1}` (квантификатор)\
`a*` - `a{0,}` | `a+` - `a{1,}`\
`.` - любой символ (за исключением `\n`)\
`\s` - любой пробельный символ | `\S` - любой НЕ пробельный символ\
`\d` - `[0-9]` | `\D` - `[^0-9]`\
`[a-zA-Zа-яёА-ЯЁ]` - любая буква\
`\w` - `[0-9a-zA-Z_]` | `\W` - `[^0-9a-zA-Z_]`

### Шаблоны позиции
`^` - начало текста; `$` - конец текста\
`\b` - начало/конец слова; `\B` - не начало/конец слова\
`A(?=B)` - A перед B; `A(?!B)` - A не перед B\
`(?<=A)B` - B после A; `(?<!A)B` - B не после A

```python
import re

re.split(r'a', 'bbababbb')  # ['bb', 'b', 'bbb']
re.split(r'\s*([+\-*/])\s*', '2 + 5*1.3')  # ['2', '+', '5', '*', '1.3']

re.sub(r'\d\d\.\d\d\.\d{4}', 'DD.MM.YYYY', '05.04.1242 и 08.09.1380')  # 'DD.MM.YYYY и DD.MM.YYYY'
re.sub(r'(\d\d)\.(\d\d)\.(\d{4})', r'\2.\1.\3', '05.04.1242 и 08.09.1380')  # '04.05.1242 и 09.08.1380'
re.sub(r'\b[х]\w*', lambda match: f'~{match[0]}~', 'а ты хорош!')  # 'а ты ~хорош~!'
re.sub(r'\b(\w+)\b\W\1', '\\1', 'привет привет программист-программист')  # привет программист \\ так как не r''

re.findall(r'\d{2}', '12ab34cd5f')  # ['12', '34']
regexp : re.Pattern = re.compile(r'([a-z]+)(\d+)')
regexp.findall('ab12, cd34')  # [('ab', '12'), ('cd', '34')]

# найти все пересекающиеся вхождения
pattern = re.compile('(?=(abab))')  # positive lookahead 
for match in re.finditer(pattern, 'abababab'):
    print(match.start())  # 0, 2, 4

phone = 'Телефон +7 (000) 111 22 33'
match: re.Match = re.search(r'(\d\d)\D(\d\d)', phone)
print(match[0], ':', match[1], ':', match[2])  # not iterable  # 11 22 : 11 : 22
print(' : '.join(phone[match.start(i):match.end(i)] for i in range(3)))  # 11 22 : 11 : 22

strings = ['12', '12a', 'a12']
regex = re.compile(r'\d{2}')
# search - любое совпадение
results = list(filter(lambda row: regex.search(row), strings))  # ['12', '12a', 'a12']
# match - совпадение в начале строки
results = list(filter(lambda row: regex.match(row), strings))  # ['12', '12a']
# fullmatch - полное строки
results = list(filter(lambda row: regex.fullmatch(row), strings))  # ['12']
```


## typing

Цель типизации – указать разработчику на ожидаемый тип данных.

**mypy** – синтаксический анализатор **аннотаций**.

```shell
python -m pip install mypy
```

```
# mypy.ini

[mypy]
disallow_untyped_defs = True  # запрещает объявлять функции без указания типов
ignore_missing_imports = True
```

**generic** – специальные типы, в которых можно указывать внутренние типы.

```python
from typing import Optional

def greeting(name: Optional[str]) -> str:
   return 'Hello ' + name
```

`Any` – любой тип\
`Union[int, float]` – или `int | float`\
`Optional[str]` – или None\
`Type[A]` – экземпляр класса A или дочернего от него\
`dict[str, int]` – словарь, где ключи будут иметь тип str, а значения - тип int\
`iterable[int]` – переменные, созданные генераторами или итераторами\
`Literal['A'] | Literal['B']` – выбор из значений