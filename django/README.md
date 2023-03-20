# [Django](https://www.djangoproject.com/)

\- Веб-фреймворк для создания сайтов.\
В отличии от микрофреймворка Flask, Django нуждается в меньшем количестве ручной настройки приложения и не нуждается в дополнительных пакетах для работы с ORM.

<img src="images/django.jpeg" alt="logo django" title="Logo django" style="height: 240px;" />

Django построен по принципу **MVC**, но именуется **MTV**:
* Model - отображение данных в ООП формат $\rightarrow$ **Model**
* View - визуальная составляющая $\rightarrow$ **Template**
* Controller - бизнес-логика приложения $\rightarrow$ **View**

Приложение разделено на app-ы, python-пакеты, оформленные специальным образом, являющиеся небольшими отдельными web-приложениями.\
Файл `manage.py` - консольная утилита, с помощью которой создаются папки и файлы, генерируется шаблонный код, накатываются миграции, запускается приложение.


## poetry

\- своременный пакетный менеджер, не такой "примитивный" как pip.

```shell
pip install poetry  :: установить
poetry init  :: создание pyproject.toml

poetry install  :: установить все зависимости
```

```shell
poetry add django  :: pip install django
```


### Виртуальное окружение `virtualenvwrapper`

```shell
python -m pip install virtualenvwrapper
:: python -m pip install virtualenv

python -V  :: узанть версию
which python  :: узнать расположение интерпертатора
export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
export VIRTUALENVWRAPPER_VIRTUALENV=/usr/local/bin/virtualenv
source /usr/local/bin/virtualenvwrapper.sh
```

```shell
mkvirtualenv <name_project>

mkdir <name_project>
cd <name_project>
:: создать poetry

:: python -m venv env 
:: source ./env/bin/activate
deactivate
```


## Создать Django-приложение

```shell
django-admin startproject <name_project> .
./manage.py startapp <name_app>  :: создать отдельный функционал
./manage.py runserver  :: запустить сервер
```


## Создать модель

Модель - это класс, который описывает поля (столбцы) таблицы DB.

```python
# name_app/models.py
from django.db import models

class M(models.Model):
    text = models.CharField(max_length=100)
```

**Миграция** фиксирует текущее состояние DB.

```shell
./manage.py makemigrations
./manage.py migrate  :: накатить
```


## Создать URL

соеденить адреса с views

```python
# name_project/urls.py
from django.contrib import admin
from django.urls import path
from name_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('items/', views.index),
    path('items/<int:item_id>', views.get),
]
```

Допустимые параметры:
- `str` — любая непустая строка.
- `int` — 0 или любое положительное число.
- `slug` — строка из ASCII букв или чисел, а также дефисы и подчеркивание.
- `uuid` — универсальный уникальный идентификатор.
- `path` — непустая строка, включая /.


## Создать view

```python
# name_app/views.py
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from name_app.models import M

def hello(request):
    return HttpResponse('Hello world')
```

### вытащить path-параметры

```python
def get(request, item_id):
    if request.method == 'GET':
        try:
            vacancy = M.objects.get(pk=item_id)
        except Vacancy.DoesNotExist as exc:
            return JsonResponse({'error': str(exc)}, status=404)
        
        return JsonResponse({
            'id': item_id,
            'text': item.text,
        }, json_dumps_params={"ensure_ascii": False})  # Кодировка
```


## GET запрос

```python
def index(request):
    if request.method == 'GET':
        items = M.objects.all()

        if search_text := request.GET.get("text"):  # принимает query-параметр
            items = items.filter(text=search_text)

        response = []
        for item in items:
            response.append({
                'id': item.id,
                'text': item.text,
            })

        return JsonResponse(response, safe=False,  # Передаем не словарь
                            json_dumps_params={"ensure_ascii": False})
```
