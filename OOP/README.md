# ООП

**Объектно-Ориентированное Программирование** - стиль (парадигма, методология) программирования, в которой все важные вещи представлены объектами,
каждый из которых является экземпляром определенного класса, а классы образуют иерархию наследования.\
Это делает код более модульным и повторно используемым.

Является противопоставлением *функциональному (процедурному)*, где существует жесткое разделение между данными и функциями.

**Абстракция** - представление из полей и методов объектов, которые описывают реальные физические объекты.\
**Классы** - (реализация абстракций) шаблоны для создания объектов (*экземпляров класса*).\
Класс определяет атрибуты и методы объекта, а экземпляр представляет собой конкретный экземпляр этого объекта,
который может иметь свои собственные значения атрибутов.\
**Интерфейс** - набор публичных методов, через которые можно взаимодействовать с объектом.

*ООП* базируется на принципах:


## Инкапсуляция

– это способность объектов скрывать часть своего состояния и поведения от прямого доступа извне,
предоставляя внешнему миру только определённый интерфейс («контракт» взаимодействия объектов).\
Это позволяет защитить данные от случайных изменений.

```python
class Account:
    def __init__(self, balance):
        self.__balance = balance

    def _storage(self):
        print('hided')

    def get_balance(self):
        return self.__balance

    def set_balance(self, balance):
        self._storage()  # underscore (защищенные)
        self.__balance = balance  #  dunder (private)

        
account = Account(0)
account.set_balance(100)  # hided
print(account.get_balance())  # 100
```

Дандер-методы используются для определения специального поведения объекта в ответ на различные операции.


## Наследование

Возможность создания новых классов на основе существующих, способствуя повторному использованию полей и методов родителя.

```python
class Shape:  # наследуется от object
    def __init__(self, color):
        self.color = color
    
    def draw(self):
        print(f'Drawing a {self.color} shape')

class Circle(Shape):
    def __init__(self, color, radius):
        super().__init__(color)
        self.radius = radius

circle = Circle('red', 2)
circle.draw()  # Drawing a red shape
```


### Множественное наследование

– создание цепочки связей класснов с целью комбинирования и сочетания функциональности сразу нескольких классов в одном.

Ромбовидное наследование (diamond problem) - для определения порядка используется алгоритм поиска в ширину.

```python
class A2:
    def __init__(self):
        self.balance = 1
        
class A1(A2):
    pass
        
class B1:  # B1(A2) для формирования ромба (будет 3)
    def __init__(self):
        self.balance = 3
        
class C(A1, B1):
    pass

c = C()
print(c.balance)  # 1
issubclass(C, A2)  # True
C.mro()  # [__main__.C, __main__.A1, __main__.A2, __main__.B1, object]
```


## Полиморфизм

– свойство, при котором различные обьекты с однаковым поведением используются одним и тем же образом.\
Гибкость, то есть дочерние классы могут расширять и переопределять методы родителя.\
**overloading (перегрузка)** - это способность метода или оператора выполнять разные действия в зависимости от типа.

```python
class Square(Shape):
    def __init__(self, color, width):
        super(Square, self).__init__(color)
        self.width = width
        
    def draw(self):
        super(Square, self).draw()
        print(f'Drawing a square with width={self.width}')
        
        
shapes = [Circle('blue', 7), Square('red', 5)]
for shape in shapes:
    shape.draw()
```


## Абстракция

– это модель некоего объекта или явления реального мира, в которой опущены незначительные детали, не играющие существенной роли в данном контексте.

Классы могут определять общие свойства и методы для группы объектов.

```python
from abc import ABC, ABCMeta, abstractmethod 

class A(ABC):  # class A(metaclass=ABCMeta)
    def __init__(self):
        pass

    @abstractmethod
    def am(self):  # сигнатура
        pass

class B(A):    
    def __init__(self):
        pass
    
    def am(self):
        pass
```


## Композиция

Сложные объекты, созданные из простых.

```python
class Car:
    def init(self):
        self.engine = Engine()
        self.wheels = [Wheel() for _ in range(4)]
        self.body = Body()
        
    def start(self):
        self.engine.start()
```

***


## Замыкания

– это функция, которая запоминает значения из своего лексического контекста, то есть на момент создания.

```python
def outer_function(x):
    def inner_function(y):
        return x + y
    return inner_function

add_five = outer_function(5)
print(add_five(3))  # 8
```

```python
def add_to(elem, collection=[]):  # collection=None
    # collection = collection or []
    collection.append(elem)
    return collection

print(add_to('a'))  # ['a']
print(add_to('b'))  # ['a', 'b']
```


## Декоратор

– это инструмент, при котором одна функция принимает в качестве аргумента другую функцию, и оборачивает её новой функцией, что расширяет функциональность без непосредственного изменения кода декарируемой функции.

```python
from functools import wraps

def count_calls(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        """Oh, No"""
        wrapper.calls += 1
        result = func(*args, **kwargs)
        return result
    wrapper.calls = 0
    return wrapper

@count_calls
def my_func():
    """Docstring"""
    pass
# my_func = count_calls(my_func)

my_func()
my_func()
print(my_func.calls)  # 2
print(my_func.__name__, my_func.__doc__)  # my_func Docstring
```

Декоратор с параметрами:
```python
def decor_count_calls(start):
    def count_calls(func):
        def wrapper(*args, **kwargs):
            ...
        wrapper.calls = start
        return wrapper
    return count_calls

@decor_count_calls(2)
def my_func():
    pass
```

---

Магические (**dunder**) методы нужны для реализации свойств объектов при их взаимодействии.

```python
class Cls():
    """description"""  # Cls.__doc__
    
    count = 0
    
    def __init__(self, name, age):  # конструктор, его вызывает __new__
        self.name = name  # self - ссылка на экземпляр
        self._age = age
        
    @staticmethod # методу не требуется доступ к свойствам экземпляра
    def say_greetings():
        pass
    
    @classmethod # метод вызывается через класс
    def say_greetings(cls):
        pass
        
    @property # метод выглядит как атрибут
    def age(self):
        return self._age
    
    @age.setter
    def age(self, value):
        if value < 0:
            raise ValueError('Age cannot be negative')
        self._age = value
        
    @age.deleter
    def age(self):
        del self._age
        
    def __call__(self, *args, **kwars):  # вызывается
        return
    
    def __str__(self):  # вызывается при print
        return f'I\'m {self.name}'
    
    def __repr__(self):  # вызывается для отладки
        return f'{self.name}'

    
ins = Cls('A', 18)
isinstance(ins, Cls)  # True
```

### with

– менеджер контекста

включает в себя dunder методы: `__enter__` и `__exit__`, заменяет try/except и **close()** в finally.

```python
with open(file_path, 'w') as file:
    file.write(text)
    
# 'a' -  дописать в конец
# 'b' -  бинарный режим

with open(file_path, 'r') as file:
    # line = file.readline()
    for line in file:
        print(line.rstrip())
```

---

Итерируемые объекты (iterable) — это любые объекты, предоставляющий возможность поочередно перебрать элементы, которые будут вычисляться по мере необходимости.\
Экономят использование памяти и процессорного времени.\
Итерируемые объекты – это экземпляры тех классов, которые имеют магические методы `__iter__` и `__next__`.

```python
...
class Iter:
    def __init__(self, stop_number):
        self.stop_number = stop_number
        self.count = 0
        
    def __iter__(self):
        return self

    def __next__(self):
        count = self.count
        if count >= self.stop_number:
            raise StopIteration
        self.count += 1
        return count

my_iter = iter(Iter(4))
print(next(my_iter))
# [x for x in Iter(4)]
```

Ключевое отличие между итерируемыми объектами и итераторами заключается в том, что итераторы имеют внутреннее состояние (итерации), запоминающее текущую позицию в последовательности.

Генератор - типичный способ создания итератора.

```python
def generator(numbers):
    num = 0
    while num < numbers:
        yield num
        num += 1
        
my_iter = generator(4)
```
