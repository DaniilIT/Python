# Тестирование

### Django тестирование

```python
from django.test import TestCase

class ItemTestCase(TestCase):
    def setUp(self):
        Item.objects.create(...)
    
    def test_item(self):
        """Test Item"""
        item = Item.objects.get(...)
        self.assertEqual(item.method(), 'result')
`

### DRF тестирование

```python
from django.urls import revercse
from django_framework import status
from django_framework.test import APITestCase

class ItemTests(APITestCase):
    def setUp(self):
        Item.objects.create(...)
    
    def test_create_tem(self):
        """Ensure we can create a new item object"""
        url = reverce('account-list')
        data = {'name': 'item_name'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Item.objects.count(), 1)
        self.assertEqual(Item.objects.get().name, data['name'])
```


## pytest

```sh
poetry add pytest-django
```

Для настройки необходимо указать в директиве `pytest` константу `DJANGO_SETTINGS_MODULE`:
```
# pytests.ini 

[pytest]
DJANGO_SETTINGS_MODULE = project_name.settings
```

<img src="images/pycharm.png" alt="pycharm" title="pycharm" style="height: 380px;" />

**client** - фикстура для запросов.

```python
# tests/simple_test.py
def test_root_not_found(client):
    response = client.get('/')
    assert response.status_code == 404
```

Запуск:
```sh
python -m pytest
```


## Параметризация

`@pytest.mark.parametrize` - декоратор, который используется когда eсть несколько тестов с одинаковым кодом, который отличается только значением нескольких параметров.

```python
@pytest.mark.parametrize("test_input,expected", [("1+1", 2), ("1+2", 3)])
def test_eval(test_input, expected):
    assert eval(test_input) == expected
```


## Фикстуры 

\- блок кода, обернутый в декоратор `@pytest.fixture()`, который затем можно использовать как аргумент для функции-теста.

```python
# tests/fixtures.py
import pytest

@pytest.fixture
@pytest.mark.django_db
def token(client, django_user_model):
    username = 'user'
    password = 'password'

    # django_user_model - фикстура для создания пользователей
    django_user_model.objects.create_user(
        username=username, password=password, role='admin'
    )

    response = client.post(
        '/user/login/',
        {'username': username, 'password': password},
        format='json' 
    )
    return response.data['token']
```

Подключить фикстуру:
```python
# tests/conftests.py
pytest_plugins = 'tests.fixtures'
```

`@pytest.mark.django_db` - декоратор для сохранения записей в DB до теста, проверки сохранились ли они и очистки их после завершения теста.

```python
# tests/app_name/item_create_test.py
from datetime import date
import pytest

@pytest.mark.django_db
def test_create_item(client, token):
    data = {'text': 'text'}

    response = client.post(
        '/app_name/create/',
        data,
        content_type='application/json',  # format='json'
        HTTP_AUTHORIZATION='Token ' + token
    )
    
    expected_response = {
        'id': 1,
        'text': 'text',
        'created': date.today().strftime('%Y-%m-%d'),
        ...
        'user': None,
    }

    assert response.status_code == 201
    assert response.data == expected_response
```


## Фабрика

\- класс, на основе которого будут генерироваться и предзаполняться данными модели в тестах.\
Фабрики также могут использоваться в качестве фикстур.

```sh
poetry add pytest-factoryboy
```

```python
# tests/factories.py
import factory.django

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker('name')  # генерация неповторяющихся имен
    password = 'password'

class ItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Item

    text = 'test text'
    user = factory.SubFactory(UserFactory)
```

Подключить фабрику:
```python
# tests/conftests.py
from pytest_factoryboy import register
from tests.factories import UserFactory, ItemFactory

pytest_plugins = 'tests.fixtures'

register(UserFactory)
register(ItemFactory) 
```

создадутся фикстуры по названию без 'Factory' и в нижнем регистре (строчными): user, item

```python
# tests/app_name/item_detail_test.py
from datetime import date
import pytest

@pytest.mark.django_db
def test_app_name_detail(client, item, token):
    # item = Item.objects.create(text='test text')

    response = client.get(
        f'/app_name/{item.pk}/',
        HTTP_AUTHORIZATION='Token ' + token
    )
    
    expected_response = {
        'id': vacancy.pk,
        'text': vacancy.text,
        'created': date.today().strftime('%Y-%m-%d'),
        ...
        'user': vacancy.user_id,
    }

    assert response.status_code == 200
    assert response.data == expected_response
```

### Использование фабрики для создание списка

```python
# tests/app_name/item_list_test.py
@pytest.mark.django_db
def test_vacancy_list(client):
    items = ItemFactory.create_batch(10)

    response = client.get('/app_name/')
    
    expected_response = {
        'count': 10,
        'next': None,
        'previous': None,
        'results': ItemListSerializer(items, many=True).data
    }

    assert response.status_code == 200
    assert response.data == expected_response
```
