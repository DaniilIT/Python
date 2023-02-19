# [PYTEST](https://docs.pytest.org/en/latest/)

\- стандарт в написании автоматических тестов.

<img src="images/pytest.svg" alt="logo pytest" title="Logo pytest" style="height: 380px;" />

Exceptions (исключения) - ошибки, возникающие в ходе выполнения программы.

[BaseException]
$$ \Downarrow $$
[Exception][SystemExit][KeyboardInterrupt]
$$ \Downarrow $$
[SyntaxError][NameError][ValueError][TypeError][ZeroDivisionError][IndexError][КеуЕггог]...

Обработчик ошибок
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

1. pytest собирает по всему дереву проекта файлы, функции и классы похожие на тесты.
2. ищет файлы, которые начинаются на `test_` или заканчиваются на `_test.py`.
3. выполняет все asserts, а не останавливается на первом

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

```
pytest
```

Параметризация
```python
import pytest
from utils import my_function

my_function_parameters = [(0, 0, 1), (1, 2, 6), (1, -1, 0)]

@pytest.mark.parametrize('first, second, expected', my_function_parameters)
def test_my_function(first, second, expected):
    assert my_function(first, second) == expected, f'my_function is wrong for {first} and {second}'
```

Используем класс
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

---

Тестируем типы исключений
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

@pytest.mark.parametrize('radius, exception', get_circle_square_exceptions)
def test_type_error_get_circle_square(radius, exception):
    with pytest.raises(exception):
        get_circle_square(radius)
```

---

Тестируем класс
```python
# dao.ру
import math

class Circle:
    def __init__(self, radius):
        if type(radius) not in [int, float]:
            raise TypeError(f'expected radius type int or float, but got: {type(radius)}')
        if radius < 0:
            raise ValueError(f'expected radius greater 0, but got: {radius}')
        self.radius = radius
    
    def get_perimeter(self):
        return math.pi * radius ** 2
```

```python
# dao_test.ру
import pytest
from dao import Circle

# circle_parameters = [(1, 2), (1, 6.28), (1, -1, 0)]

class TestCircle:
    def test_get_perimeter(self):
        circle = Circle(1)
        assert round(circle.get_perimeter(), 2) == 6.28, 'Circle is wrong on get_perimeter for radius=1'
        
    def test_type_error_init(self):
        with pytest.raises(TypeError):
            get_circle_square('1')
```

**Фикстурa** - функция, которая выполняется до тестирования для подготовки данных. 

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
        assert my_function(some_test_data[0]) == some_test_data[1], f'my_function is wrong for {some_test_data[0]}'
```


## DAO (Data Access Object)

\- объект для доступа к данным из файлов, базы данных или сторонних сервисов.

```python
# candidate.ру

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
# candidates_dao.ру
import json
from candidate import Candidate

class CandidatesDAO:
    def __init__(self, path):
        """ При создании нужно указать путь к файлу с данными
        """
        self.path = path
        
    def load_data(self):
        candidates = []
        with open(self.path, 'r', encoding='utf-8') as file:
            candidates_data = json.load(file)

            for candidate in candidates_data:
                candidates.append(Candidate(
                    candidate.get('id'),
                    candidate.get('name'),
                    candidate.get('position'),
                    candidate.get('skills')
                ))
        return candidates

    def get_all(self):
        """ Возвращает список со всеми кандидатами
        """
        candidates = self.load_data()
        return candidates

    def get_by_skill(self, skill):
        candidates = self.load_data()
        skilled_candidates = []
        skill_lower = skill.lower()

        for candidate in candidates:
            candidate_skills = candidate.skills.lower().split(', ')
            if skill_lower in candidate_skills:
                skilled_candidates.append(candidate)
                
        return skilled_candidates

    def get_by_id(self, candidate_id):
        """ Возвращает одного кандидата по его id
        """
        candidates = self.load_data()
        for candidate in candidate:
            if candidate.id == candidate_id:
                return candidate
```

```python
# app.py
from candidates_dao import CandidatesDAO

candidates_dao = CandidatesDAO()

@app.route('/')
def index_page():
    candidates = candidates_dao.get_all()
    return render_template('index.html', candidates=candidates)

@app.route('/skill/<skill>')
def skill_page(skill_name):
    candidates = candidates_dao.get_by_skill(skill)
    return render_template('skill.html', candidates=candidates)

@app.route('/candidate/<int:uid>')
def skill_page(uid):
    candidate = candidates_dao.get_by_id(uid)
    return render_template('candidate.html', candidate=candidate)
```

## для FLASK

```python
#conftest.py

import pytest
import app

@pytest.fixture()
def test_client():
    app = app.app
    return app.test_client()  # сервер не поднимает, но запросы выполняет
```

```python
#main_test.py
import pytest

class TestMain:
    def test_root_status(self, test_client):
        """ Проверяем при запросе кандидатов нужный статус код
        """
        response = test_client.get('/', follow_redirects=True)
        assert response.status_code == 200, 'Статус код не верный'
        
    def test_root_content(self, test_client):
        response = test_client.get('/', follow_redirects=True)
        assert 'Это главная страничка' in response.data.decode('utf-8'), 'Контент не верный'
        
    def test_json_json(self, test_client):
        response = test_client.get('/json/', follow_redirects=True)
        assert response.json.get('name') == 'Daniil', 'Имя получено неверно'
        
    def test_search(self, test_client):
        params = {'s': 'cat'}
        response = test_client.get('/search', query_string=params)
        assert response.status_code == 200, 'Статус код не верный'
        assert len(response.json) == 3
        
    def test_form(self, test_client):
        data = {'name': 'Daniil'}
        response = test_client.post('/form', json=data)
        assert response.status_code == 200, 'Статус код не верный'
        assert len(response.json) == 3

```

```python
# candidates_dao_test.py
import pytest
from арр.candidates.dao.candidate_dao import CandidateDAO

@pytest.fixture()
def candidate_dao():
    candidate_dao_instance = CandidateDAO('./data/candidates.json')
    return candidate_dao_instance

# Ключи, которые ожидаем у кандидата
KEY_SHOULD_BE = {'pk', 'name', 'position'}

class TestCandidateDAO:
    def test_get_all(self, candidates_dao):
        """ Проверяем, верный ли список кандидатов возвращается
        """
        candidates = candidates_dao.get_all()
        assert type(candidates) == list, 'возвращается не список'
        assert len(candidates) > 0, 'возвращается пустой список'
        assert set(candidates[0].keys()) == KEY_SHOULD_BE, 'неверный список'
        
    def test_get_by_id(self, candidates_dao):
        """ Проверяем, верный ли кандидат возвращается при запросе одного
        """
        candidate = candidates_dao.get_by_id(1)
        assert type(candidate) == dict, 'возвращается не словарь'
        assert candidate['pk'] == 1, 'возвращается неправильный кандидат'
        assert set(candidate.keys()) == KEY_SHOULD_BE, 'неверный список'

    def test_root_status(self, test_client):
        response = test_client.get('/', follow_redirects=True)
        assert response.status_code == 200, 'Статус код не верный'
        
    def test_root_content(self, test_client):
        response = test_client.get('/', follow_redirects=True)
        assert 'Это главная страничка' in response.data.decode('utf-8'), 'Контент не верный'
```















