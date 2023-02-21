# [PYTEST](https://docs.pytest.org/en/latest/)

\- стандарт в написании автоматических тестов.

<img src="images/pytest.svg" alt="logo pytest" title="Logo pytest" style="height: 380px;" />

Exceptions (исключения) - ошибки, возникающие в ходе выполнения программы.

<div align="center"> [BaseException] </div>

$$\Downarrow$$

<div align="center"> [Exception] &emsp; [SystemExit] &emsp; [KeyboardInterrupt] </div>

$$\Downarrow$$

<div align="center"> SyntaxError &ensp; NameError &ensp; ValueError &ensp; TypeError &ensp; ZeroDivisionError &ensp; IndexError &ensp; КеуЕггог... </div>


## Обработчик ошибок:

```python
class MyException(Exception):
    # pass
    def __init__(self, message=None):
        super().__init__(message)
        self.message = message

try:
    a = int(input('a = '))
    if a % 2:
        raise MyException("even number expected")
    b = 100 / a
except (ZeroDivisionError, ValueError) as error:
    print(error) # invalid literal for int() with base 10: ''
except MyException:
    raise # проброс наверх
else: # для цикла выполнится, если не прервался с break
    print(f'b = {b}')
finally:
    print('конец')
```

## тестирование

1. Unit - модульное тестирование функций и классов.
2. Интеграционное - тестирование связи с внешними источниками, API, баз данных.
3. UI - тестирование производительности, защищенности и надежности.


## Assert

```python
assert 2 + 2 == 4, 'count is wrong'
# (if False) AssertionError: count is wrong
```

```
OPTIMIZE - отключает проверку условий assert
python -O main.py
```

***

```
pip install pytest
```

* pytest собирает по всему дереву проекта файлы, функции и классы похожие на тесты:\
    ищет файлы, которые начинаются на `test_` или заканчиваются на `_test.py`;
* выполняет функции и методы с префиксом `test`, классы с префиксом `Test` без конструктора `__init__`;
* выполняет все asserts, а не останавливается на первом;

```python
# utils_test.ру
import pytest
from utils import my_function

def test_my_function_1():
    assert my_function(1) == 2, 'my_function is wrong for 1'

def test_my_function_2():
    assert my_function(2) == 4, 'my_function is wrong for 2'
    
def test_my_function_3():
    assert my_function(3) == 8, 'my_function is wrong for 3'
```

Запуск:
```
pytest
# или (можно без tests/__init__.py)
python -m pytest
```


## Параметризация

```python
# utils_test.ру
import pytest
from utils import my_function

my_function_parameters = [(0, 0, 1), (1, 2, 6), (1, -1, 0)]

@pytest.mark.parametrize('first, second, expected', my_function_parameters)
def test_my_function(first, second, expected):
    assert my_function(first, second) == expected, f'my_function is wrong for {first} and {second}'
```

Используем класс:

```python
# utils_test.ру
import pytest
from utils import my_function

my_function_parameters = [(0, 0, 1), (1, 2, 6), (1, -1, 0)]

class TestMyFunction:
    @pytest.mark.parametrize('first, second, expected', my_function_parameters)
    def test_my_function(self, first, second, expected):
        assert my_function(first, second) == expected, f'my_function is wrong for {first} and {second}'
```


## Тестируем типы исключений

```python
# utils.ру
import math

def get_circle_square(radius):
    if type(radius) not in [int, float]:
        raise TypeError(f'expected radius type int or float, but got: {type(radius)}')
    if radius < 0:
        raise ValueError(f'expected radius greater 0, but got: {radius}')
    return math.pi * radius ** 2
```

```python
# utils_test.ру
import pytest
from utils import get_circle_square

get_circle_square_exceptions = [('', TypeError), (-1, ValueError)]

class TestGetCircleSquare:
    @pytest.mark.parametrize('radius, exception', get_circle_square_exceptions)
    def test_type_error_get_circle_square(self, radius, exception):
        with pytest.raises(exception):
            get_circle_square(radius)
```

## Тестируем класс

```python
# utils.ру
import math

class Circle:
    def __init__(self, radius):
        if type(radius) not in [int, float]:
            raise TypeError(f'expected radius type int or float, but got: {type(radius)}')
        if radius < 0:
            raise ValueError(f'expected radius greater 0, but got: {radius}')
        self.radius = radius
    
    def get_perimeter(self):
        return math.pi * self.radius ** 2
```

```python
# utils_test.ру
import pytest
from utils import Circle

class TestCircle:
    def test_get_perimeter(self):
        circle = Circle(1)
        assert round(circle.get_perimeter(), 2) == 6.28
        
    def test_type_error_init(self):
        with pytest.raises(TypeError):
            Circle('1')
```


## Фикстурa

\- функция, которая выполняется до тестирования для подготовки данных. 

```python
# conftest.ру
import pytest

@pytest.fixture()
def some_test_data():
    return (1, 1)
```

```python
# utils_test.ру
import pytest
from utils import my_function

class TestMyFunction:
    def test_my_function(self, some_test_data):
        assert my_function(some_test_data[0]) == some_test_data[1]
```


## DAO

**Data Access Object** - объект для доступа к данным из файлов, базы данных или сторонних сервисов.

```python
# dao/candidate.ру

class Candidate:
    def __init__(self, candidate_id, name, position, skills):
        self.id = candidate_id
        self.name = name
        self.position = position
        self.skills = skills

    def __repr__(self):
        return f'{self.name}'
```

```python
# dao/candidates_dao.ру
import json
from .candidate import Candidate

class CandidatesDAO:
    def __init__(self, path):
        """ При создании нужно указать путь к файлу с данными
        """
        self.path = path
        
    def load_data(self):
        """ Возвращает всех кандидатов
        """
        candidates = []
        with open(self.path, 'r', encoding='utf-8') as json_file:
            raw_candidates = json.load(json_file)

            for candidate in raw_candidates:
                candidates.append(Candidate(
                    candidate.get('id'),
                    candidate.get('name'),
                    candidate.get('position'),
                    candidate.get('skills')
                ))
        return candidates

    def get_by_id(self, candidate_id):
        """ Возвращает одного кандидата по его id
        """
        candidates = self.load_data()
        for candidate in candidates:
            if candidate.id == candidate_id:
                return candidate
```

Тест DAO:
```python
# candidates_dao_test.py
import pytest
from modules.candidates.dao.candidate import Candidate
from modules.candidates.dao.candidate_dao import CandidateDAO


@pytest.fixture()
def candidate_dao():
    candidate_dao_instance = CandidateDAO('./data/candidates.json')
    return candidate_dao_instance


class TestCandidateDAO:
    def test_get_all(self, candidates_dao):
        """ Проверяем, верный ли список кандидатов возвращается
        """
        candidates = candidates_dao.get_all()
        assert isinstance(candidates, list)
        assert len(candidates) > 0
        assert isinstance(candidates[0], Candidate)
        
    def test_get_by_id(self, candidates_dao):
        """ Проверяем, верный ли кандидат возвращается при запросе одного
        """
        candidate = candidates_dao.get_by_id(1)
        assert isinstance(candidate, Candidate)
        assert candidate.id == 1
```


## FLASK

```python
#conftest.py
import pytest
from app import app

@pytest.fixture()
def test_client():
    return app.test_client()  # сервер не поднимается, но на запросы отвечает

@pytest.fixture()
def key_should_be():
    return {'name', 'pk'}
```

Тест views:
```python
#main_test.py
import pytest

class TestMain:
    def test_root_status(self, test_client):
        response = test_client.get('/', follow_redirects=True)
        assert response.status_code == 200
        
    def test_root_content(self, test_client):
        response = test_client.get('/', follow_redirects=True)
        assert 'Это главная страничка' in response.data.decode('utf-8')
        
    def test_json_data(self, test_client, key_should_be):
        response = test_client.get('/json/', follow_redirects=True)
        assert set(response.json.keys()) == key_should_be
        
    def test_search(self, test_client):
        params = {'s': 'cat'}
        response = test_client.get('/search', query_string=params)
        assert response.status_code == 200
        
    def test_form(self, test_client):
        data = {'name': 'Daniil'}
        response = test_client.post('/form', json=data)
        assert response.status_code == 200
```
