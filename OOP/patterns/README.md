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
* Open/Closed Principle \
    Принцип открытости/закрытости (Класс должен быть открытым для расширения и закрытым для изменения)
* Liskov Substitution Principle \
    Принцип подстановки (на подтипы) (Методы должны быть с ожидаемым поведением)
* Interface Segregation Principle \
    Принцип разделения интерфейса (Лучше несколько специфичных классов, нежели один огромный)
* Dependency Inversion Principle \
    Принцип инверсии зависимостей (Высокоуровневые модули не должны зависеть от низкоуровневых модулей (Поля классов должны устанавливаться через конструктор))

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

```python
import re

re.split('a', 'bbabbbab')  # ['bb', 'bbb', 'b']

string = '12da32fd4fw'
strings = ['12', '12a', 'a12']
pattern = r'\d{2}'

print(re.findall(pattern, string))  # ['12', '32']
result = re.search(pattern, string)  # <re.Match object; span=(0, 2), match='12'> 

# найти все пересекающиеся вхождения
pattern = re.compile('(?=(abab))')  # positive lookahead 
for match in re.finditer(pattern, 'abababab'):
    print(match.start())  # 0, 2, 4

regex: re.Pattern = re.compile(pattern)
# search - любое совпадение
result = list(filter(lambda row: regex.search(row), strings))  # ['12', '12a', 'a12']
# match - совпадение в начале строки
result = list(filter(lambda row: regex.match(row), strings))  # ['12', '12a']
# fullmatch - полное строки
result = list(filter(lambda row: regex.fullmatch(row), strings))  # ['12']
```

`[abc]` - `(a|b|c)`\
`[^abc]` - `(^a|^b|^c)`\
`[6-9]` - `(6|7|8|9)`\
`[a-z]` - любая строчная буква\
`[a-zA-Z]` - любая буква\
`a{2}` - aa\
`a{1,3}` - или a, или aa, или aaa\
`a?` - `a{,1}` (квантификатор)\
`a+` - `a{1,}`\
`a*` - `a{0,}`\
`.` - любой символ\
`^` - начало текста\
`$` - конец текста\
`\b` - начало / конец слова\
`\s` - любой пробельный символ\
`\S` - любой НЕ пробельный символ\
`\d` - `[0-9]`\
`\D` - `[^0-9]`\
`\w` - `[0-9a-zA-Z_]`\
`\W` - `[^0-9a-zA-Z_]`


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
