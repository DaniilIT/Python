# [Flask](https://flask.palletsprojects.com/en/latest/)

– микрофреймворк для создания веб приложения.

<img src="images/flask.webp" alt="logo flask" title="Logo flask" style="height: 240px;" />

*Модуль* – это файл, который содержит исполняемый код на python.\
*Пакет* – набор модулей, папка, которая содержит файл `__init__.py` в качестве флага.\
*Библиотека* – набор пакетов.\
**Фреймворк** – набор готовых компонентов (библиотек), из которых формируется приложение.

$\Leftrightarrow$ [Веб-приложение] $\Leftrightarrow$ [WSGI-сервер] $\Leftrightarrow$ [Flask-приложение]

Flask включает в себя работу с:
* маршрутами и методами
* статическими файлами
* загрузкой файлов
* JSON-данными
* шаблонами
* cookies и сессиями
* тестами

```sh
pip install Flask
```

```python
from flask import Flask

app = Flask(__name__)  # указать, где искать ресурсы


@app.route('/')  # маршрутизация - связь функции с URL-адресом
def index_page():  # названия функций должны быть уникальными
    return '<p>Hello, World!</p>'  # возвращает только строку html
# app.add_url_rule('/', view_func=index_page)  # без декоратора

@app.route('/post/<int:post_id>/') # переменные
def show_post(post_id):
    return f'Post {post_id}'

if __name__ == '__main__':  # для команды flask не нужно
    app.run(debug=True)
```

Если app и views написаны отдельно, то достаточно указать: `from app import app` и `import views`.

Если не ставить в конце маршрута '/', будут обрабатываться только адреса без '/'.\
Если ставить - при запросе без '/', будет перенаправление (код 308) на маршрут с '/'.

**Эндпоинт** – маршрут с указанием метода HTTP-запроса. Маршрут (URL) может иметь несколько эндпоинтов.\
**View** (представление) – функция, которая обрабатывает запрос.

```sh
python арр.ру
flask run --debug -h 0.0.0.0 -p 80
```


## PID

**Process IDentifier** – уникальный номер процесса.

Посмотреть запущенные процессы и отфильтровать: `ps aux | grep python`.

Посмотреть, свободен ли определенный порт: (List Of Opened Files) `lsof -i -P | grep :5000`.

Убить процесс по PID: `kill 12058` или `kill -9 $(lsof -t -i:5000)`.


## [Jinjа2](https://jinja.palletsprojects.com/en/latest/)

– html-шаблонизатор.

```sh
pip install Jinja2
```

```python
from jinja2 import Environment, FileSystemLoader, select_autoescape

env = Environment(loader=FileSystemLoader('.'),
                  autoescape=select_autoescape(['html', 'xml']))  # автоэкранирование
template = env.get_template('template.html')  # найти html-шаблон

rendered_page = template.render(cards=cards, name='Daniil')

with open('./index.html', 'w', encoding='utf8') as file:
    file.write(rendered_page)
```

реализация HTTP-сервера:
```python
from http.server import HTTPServer, SimpleHTTPRequestHandler

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
```
```python
from livereload import Server

server = Server()
make_render()
server.watch('template.html', make_render)
server.serve(root='.')
```

**DOM-дерево** – иерархическое представление структуры html.

template:
```html
<a href="{{ url_for(blueprint_name.view_name, slug=slug_value) }}">{{ link_value  }}</a>
<!-- {% for index in range(6) %} -->
{% for category, drink in drinks.items() %}
    <p>{{ category }}</p>
    {% if drink.label %}{% else %}{% endif %}
{% endif %}
```

[django](https://docs.djangoproject.com/en/dev/ref/templates/builtins/)
```html
{% load static %}  <!-- settings.py `STATIC_URL ='/static/'` -->
<img src="{% static 'images/img.jpg' %}" />

<!-- #urls.py `path('', views.index, name='index')` -->
{% url 'index' slug='товар_1' %}

<!-- шаблонные фильтры -->
{{ list|length }}  <!-- подсчет длины -->
{{ text|truncate(22) }}  <!-- обрезка текста -->
{{ text|truncatechars:7 }}  <!-- обрезка текста -->
{{ html_text|safe }}  <!-- отключить экранирование -->
```

базовый шаблон:
```html
<body>
        {% block content %}
        {% endblock %}
</body>

{% extends 'blog-base.html' %}
{% block content %}
  ...
{% endblock %}
```

***


### SPA

**Single Page Application** – сервер, который отдает JSON и шаблон, а шаблонизация происходит на стороне клиента.

```python
from flask import Flask, render_template, jsonify

CARDS = [{'name': 'Daniil'}]

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['DEBUG'] = True

@app.route('/')
def index_page():
    return render_template('index.html', cards=CARDS)

@app.route('/api/')
def api_page():
    return jsonify(CARDS)

if __name__ == '__main__':
    app.run()
```


### Логирование

– ведение записей по важным для системы событиям.

```python
import logging
from flask import Flask

logging.basicConfig(filename='basic.log', level=logging.DEBUG)

app = Flask(__name__)

@app.route('/')
def index_page():
    logging.debug('Главная страница запрошена')
    return '<p>Hello, World!</p>'
```

```
DEBUG:root:Главная страница запрошена
INFO:werkzeug:127.0.0.1 - - [18/Feb/2023 16:04:37] "GET / HTTP/1.1" 200 -
```


### Обработка GET запросов

**query параметры** – данные, которые передаются в GET-запросе в формате ключ-значение, например:\
`https://translate.google.ru/?sl=ru&tl=en&op=translate`

```html
<h2>форма поиска</h2>
<form action='/search'>
    <input type='text' name='s' />
    <input type='submit' value='Найти' />
</form>
```

```python
from flask import Flask, request

app = Flask(__name__)

@app.route('/search/')
def search_page():
    s = request.args.get('s')
    return f'<p>Hello, {s}!</p>'
```


### Oбработка POST запросов

Адресная строка имеет ограничения, а данные можно передавать в теле запроса.

```html
<h2>форма</h2>
<form action='/add' method='post'>
    <input type='text' name='text' />
    <input type='submit' value='Добавить' />
</form>
```

```python
from flask import Flask, request

app = Flask(__name__)

@app.route('/add/', methods=['POST'])
def add_page():
    text = request.form.get('text')
    return f'<p>Hello, {text}!</p>'

@app.route('/add/', methods=['GET', 'POST'])
def add_page():
    # if request.method == 'GET':
    s = request.values.get('s') # values = args + form
    text = request.values.get('text')
    return f'<p>Hello, {s or text}!</p>'
```


## Работа с медиа

```html
<h2>форма загрузки</h2>
<form action='/upload/' method='post' enctype='multipart/form-data'>  <!-- кодировка -->
    <input type='file' name='picture' />
    <input type='submit' value='отправить' />
</form>
```

```python
from flask import Flask, request, redirect

ALLOWED_EXTENSIONS = {'webp', 'png', 'jpg', 'jpeg', 'gif'}

def is_filename_allowed(filename):
    """ Проверяет, что расширение файла соответствует изображению
    """
    extension = filename.split('.')[-1]  # Path(filename).suffix
    if extension in ALLOWED_EXTENSIONS:
        return True
    return False

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024  # ограничение на 2MB

@app.errorhandler(413)  # можно вызвать `abort(413)`
def entity_too_large_page(error):
    return 'Файл слишком большой', 413

@app.route('/upload/', methods=['POST'])
def upload_page():
    picture = request.files.get('picture')  # объект FileStorage
    
    if picture:
        filename = picture.filename
        # picture.name  # название поля ('picture')
        # picture.headers  # заголовки при отправке файла
        # picture.content_type  # audio/mpeg, image/png
        
        if is_filename_allowed(filename):
            picture.save(f'./uploads/{filename}')  # сохранение
            # p = picture.stream.read  # загрузка в переменную
            return '<p>Картинка сохранена</p>'
        else:
            extension = filename.split('.')[-1]
            return redirect('/error/extension', 302)
    return redirect('/error/upload', 302)
```

***


**static** – единственная папка с файлами CSS, JS, картинками и шрифтами, доступная пользователям.

Чтобы сделать содержимое другой папки доступным, нужно использовать специальную вьюшку:
```python
from flask import send_from directory

@app.route('/uploads/<path:path>')
def staticdir(path):
    return send_from_directory('uploads', path)
```


## Blueprint

– самостоятельный модуль Flask-приложения, представляющий кусок изолированной функциональности.

```
main/
- __init__.py
- views.py
- templates/
```

```python
# main/views.py
from flask import Blueprint, render_template

main_blueprint = Blueprint('main', __name__, template_folder='templates')  # 'main' используется в url_for

@main_blueprint.route('/')
def index_page():
    return render_template('index.html')
```

```python
# app.py
from flask import Flask
from main.views import main_blueprint

app = Flask(__name__)
app.register_blueprint(main_blueprint)

if __name__ == '__main__':
    app.run()
```

Можно подключать отдельную статику:\
Можно делегировать блюпринту все адреса начинающиеся на определенный префикс:
```python
# profile/views.py

profile_blueprint = Blueprint('profile', __name__, static_folder='static', template_folder='templates',
                                             url_prefix='/profile/')  # можно задать и в `app.register_blueprint(profile_blueprint, url_prefix='/profile/')`

# /profile/
@profile_blueprint.route('/')
def profile_page:
    return '<p>Hello, Profile!</p>'
```


## Конфигурация

```python
from flask import Flask
from pprint import pprint
app = Flask(__name__)
pprint(dict(app.config))
```

```
{'APPLICATION_ROOT': '/',
 'DEBUG': False,
 'ENV': 'production',
 'PROPAGATE_EXCEPTIONS': None,
 'SECRET_KEY': None,
 'SERVER_NAME': None,
 'TESTING': False,
 'JSON_AS_ASCII' = None,
 ...
}
```

```
# .env
APP_CONFIG=development
# APP_CONFIG=production
```

```python
# config.py

DEBUG = True
FLASK_ENV = 'development'
SECRET_KEY = 'secret'
TESTING = True

# или

class Config_1:
    DEBUG = True
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'
    PATH = "data.json"
```

```python
from flask import Flask
from config import Config_1

app = Flask(__name__)
app.config.from_pyfile('config.py')
# или
app.config.from_object(Config_1())
# или
app.config.from_envvar('APP_SETTINGS', silent=True)
# print(app.config.get('PATH'))

app.app_context().push()
```

### прописать путь до файла приложения в переменную окружения

```bash
export FLASK_APP=./main.py
```

### запустить приложение на определенном хосте

```bash
python3.11 -m flask run -h 0.0.0.0 -p 80
```


## Типичное файловое дерево FLASK

```
# modules/ (папка с блюпринтами)

- main/
- - __init__.py
- - templates/
- - views.ру

- blueprint_1/
- - __init__.py
- - dao/
- - templates/
- - static/
- - views.ру


data/
- data.json

- static/
- - styles/
- - scripts/
- - images/

- uploads/

- tests/
- - __init__.py
- - conftest.py
- - main_test.py
- - main_dao_test.py
- - blueprint_1_test.py
- - blueprint_1_dao_test.py

config.py (DevelopmenConfig, ProductionConfig)
app.py
setup_db.py
requirements.txt
.env
.gitignore
README.md
```

### views with DAO

```python
# modules/blueprint_1/views.ру
from flask import Blueprint, rendertemplate
from .dao.candidates_dao import CandidatesDAO  # modules.blueprint_1.dao.candidate_dao


candidates_blueprint = Blueprint('candidates_blueprint', __name__, template_folder='templates')

candidates_dao = CandidatesDAO('./data/candidates.json')


# Вьюшка для одного кандидата
@candidates_blueprint.route('/candidates/<int:pk>/')
def candidate_page(pk):
    candidate = candidates_dao.get_by_id(pk)
    return render_template('candidates_single.html', candidate=candidate)
```

### feature

```
@app.route("/someplace", strict_slashes=False)
=
@app.route("/someplace/")
@app.route("/someplace")
=
app.url_map.strict_slashes = False
```
