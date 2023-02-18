# [Flask](https://flask.palletsprojects.com/en/latest/)

\- микрофреймворк для создания веб приложения.

<img src="images/flask.webp" alt="logo flask" title="Logo flask" style="height: 380px;" />

*Модуль* - это файл, который содержит исполняемый код на python.\
*Пакет* - набор модулей, папка. Он должен содержать файл init.py в качестве флага.\
*Библиотека* - набор пакетов.\
**Фреймворк** - набор готовых компонентов (библиотек), из которых формируется приложение.

$ \Leftrightarrow $ [Веб-приложение] $ \Leftrightarrow $ [WSGI-сервер] $ \Leftrightarrow $ [Flask-приложение]

Flask включает в себя работу с:
* маршрутами и методами
* статическими файлами
* загрузкой файлов
* JSON-данными
* шаблонами
* cookies и сессиями
* тестами

```
pip install Flask
```

```python
from flask import Flask

app = Flask(__name__)  # указать, где искать ресурсы

@app.route('/')  # маршрутизация - связь функции с URL-адресом
def page_index():  # названия функций должны быть уникальными
    return '<p>Hello, World!</p>'  # возвращает только строку html
# app.add_url_rule('/', view_func=page_index)  # без декоратора

@app.route('/post/<int:post_id>/') # переменные
def show_post(post_id):
    return f'Post {post_id}'

@app.route('/card/<path:subpath>')
def show_card(subpath):
    return f'Card {subpath}'

if __name__ == '__main__':
    app.run(debug==True)
```

Если не ставить в конце маршрута '/', будут обрабатываться только адреса без '/'.\
Если ставить - при запросе без '/', будет перенаправление (код 308) на маршрут с '/'.

**Эндпоинт** - маршрут с указанием метода HTTP-запроса. Маршрут (URL) может иметь несколько эндпоинтов.\
**View** (представление) - функция, которая обрабатывает запрос.

```
python арр.ру
flask run
flask --debug run
flask --app main run  # если не app.py
```

---

Посмотреть запущенные процессы и отфильтровать: `ps aux | grep python`\
**PID** (Process IDentifier) - уникальный номер процесса.

(List Of Opened Files) Понять, свободен ли порт, который нас интересует: `lsof -i -P | grep :5000`
```
>> Python 12058 daniil 4u IPv4 0xadf36d703ab2444f 0t0 TCP localhost:5000 (LISTEN)
```

Убить процесс по PID: `kill 12058`


## [JinJа2](https://jinja.palletsprojects.com/en/latest/)

\- html-шаблонизатор.

```
pip install Jinja2
```

```python
from jinja2 import Environment, FileSystemLoader, select_autoescape

env = Environment(loader=FileSystemLoader('.'),
                  autoescape=select_autoescape(['html', 'xml']))  # автоэкранирование
template = env.get_template('template.html')  # найти html-шаблон

rendered_page = template.render(cards=cards, name='Daniil')

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)
```

реализация HTTP-сервера.
```python
from http.server import HTTPServer, SimpleHTTPRequestHandler

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
```

**DOM-дерево** - иерархическое представление структуры html.

template
```html
<!-- {% for index in range(6) %} -->
{% for category, drink in drinks.items() %}
    <p>{{ category }}</p>
    <p>{{ drink['label'] }}</p>
    {% if drink.label %}
    {% else %}
    {% endif %}
{% endif %}
```

[django](https://docs.djangoproject.com/en/dev/ref/templates/builtins/)
```html
{% load static %}  <!-- settings.py `STATIC_URL ='/static/'` -->
<img src="{% static 'images/hi.jpg' %}" />

<!-- urls.py `path('', views.index, name='index')` -->
{% url 'index' slug='газонокосилка' %}

<!-- шаблонные фильтры -->
{{ list|length }}  <!-- подсчет длины -->
{{ text|truncatechars:7 }}  <!-- обрезка текста -->
{{ html_text|safe }}  <!-- отключить экранирование -->
```

базовый шаблон
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

**SPA** (Single Page Application) - сервер отдает JSON и шаблон, а шаблонизация происходит на стороне клиента.

```python
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def page_index():
    return render_template('index.html', cards=cards)

if __name__ == '__main__':
    app.run()
```

легирования — ведения записей по важным для системы событиям.

```python
import logging
from flask import Flask

logging.basicConfig(filename='basic.log', level=logging.DEBUG)

app = Flask(__name__)

@app.route('/')
def page_index():
    logging.debug('Главная страница запрошена')
    return '<p>Hello, World!</p>'
```

```
DEBUG:root:Главная страница запрошена
INFO:werkzeug:127.0.0.1 - - [18/Feb/2023 16:04:37] "GET / HTTP/1.1" 200 -
```

### обработка query параметров

\- данные, которые передаются в GET-запросе в формате ключ-значение, например:
`https://translate.google.ru/?sl=ru&tl=en&op=translate`

```html
<h2>форма поиска</h2>
<form action='/search'>
    <input type='text' name='s'>
    <input type='submit' value='Найти'>
</form>
```

```python
from flask import Flask, request

app = Flask(__name__)

@app.route('/search/')
def page_search():
    s = request.args.get('s')
    return f'<p>Hello, {s}!</p>'
```


### обработка POST запросов

адресная строка имеет ограничения, а данные можно передавать в теле запроса.

```html
<h2>форма</h2>
<form action='/add' method='post'>
    <input type='text' name='text'>
    <input type='submit' value='Добавить'>
</form>
```

```python
from flask import Flask, request

app = Flask(__name__)

@app.route('/add/', methods=['POST'])
def page_add():
    text = request.form.get('text')
    return f'<p>Hello, {text}!</p>'

@app.route('/add/', methods=['GET', 'POST'])
def page_add():
    s = request.values.get('s')
    text = request.values.get('text')
    return f'<p>Hello, {s or text}!</p>'
```


## Работа с медиа

```html
<h2>форма загрузки</h2>
<form action='/upload/' method='post' enctype='multipart/form-data'>  <!-- кодировка -->
    <input> type='file' name='picture'>
    <input type='submit' value='отправить'>
</form>
```

```python
from flask import Flask, request

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def is_filename_allowed(filename):
    """ Проверяет, что расширение файла в белом списке.
    """
    extension = filename.split('.')[-1]
    if extension in ALLOWED_EXTENSIONS:
        return True
    return False

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024  # ограничение на 2MB

@app.errorhandler(413)  # можно вызвать `abort(413)`
def page_entity_too_large(error):
    return 'Файл слишком большой', 413

@app.route('/upload/', methods=['POST'])
def page_upload():
    picture = request.files.get("picture")  # объект FileStorage
    
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
            return '<p>Файлы с расширением {extension} не поддерживаются</p>'
    return '<p>Файл не был отправлен</p>'
```

---

**static/** - единственная папка, доступная пользователям.

Чтобы сделать содержимое другой папки доступным, нужно использовать специальную вьюшку:
```python
from flask import send_from directory

@app.route("/uploads/<path:path>")
def staticdir(path):
    return send_from_directory("uploads", path)
```


## Blueprint

/- самостоятельный пакет Flask-приложения.

```
profile\
- __init__.py
- views.py
- templates/
```

```python
from flask import Blueprint, render_template

profile_blueprint = Blueprint('profile', __name__, template_folder='templates')

@profile_blueprint.route('/profile/')
def profile_page():
    return render_template('profile_index.html')

@profile_blueprint.route('/profile/<int:user_id>')
def profile_page(int user_id):
    return f'<p>Hello, {user_id}!</p>'
```

```python
# app.py
from flask import Flask

from profile.views import profile_blueprint

app = Flask(__name__)
app.register_blueprint(profile_blueprint)

if __name__ == '__main__':
    app.run()
```

Можно делегировать блюпринту все адреса начинающиеся на определенный префикс:

```python
# app.py
app.register_blueprint(profile_blueprint, url_prefix='/profile/') # ! мб без '/' в конце

# profile/views.py
@profile_blueprint.route('/')
```




