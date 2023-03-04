# [Flask-RESTX](https://flask-restx.readthedocs.io/en/latest/index.html)

\- расширение для Flask, добавляющее поддержку быстрого создания RESTful-сервиса, основанную на Class Based View.

**Class Based View** - это способ оформения views (представлений) в виде класса.

<img src="images/flask_restx.png" alt="logo flask-restx" title="Logo flask-restx" style="height: 380px;" />

```
pip install flask-restx
```

```python
from flask import Flask, request
from flask_restx import Api, Resource

app = Flask(__name__)
api = Api(app)
api.app.config['RESTX_JSON'] = {'ensure_ascii': False, 'indent': 2}

all_ns = api.namespace('')

# @app.route('/', methods=['GET', 'POST'])
# def index_page():
#     if request.method == 'GET':
#         ...
#     elif request.method == 'POST':
#         ...
#         
# @app.route('/post/<int:post_id>/', methods=['GET', 'PUT, PATCH, DELETE'])
# def show_post(post_id: int):
#     if request.method == 'GET':
#         ...
#     elif request.method == 'PUT':
#         ...
#     elif request.method == 'PATCH':
#         ...
#     elif request.method == DELETE:
#         ...

@all_ns.route('/')
class UsersView(Resource):
    def get(self):
        all_users = User.query.all()  # SQLAlchemy
        return users_schema.dump(all_users), 200  # Marshmallow
    
    def post(self):
        req_json = request.json
        new_user = User(**req_json)
        with db.session.begin():
            db.session.add(new_user)
        return '', 201  # Created

@all_ns.route('/<int:uid>')
class UserView(Resource):
    def get(self, uid: int):
        try:
            user = User.query.filter(User.id == uid).one()
        except Exception as error:
            retrun str(error), 404
        else:
            return user_schema.dump(book), 200
    
    def put(self, uid: int):
        req_json = request.json
        try:
            user = User.query.filter(User.id == uid).one()
        except Exception as error:
            retrun str(error), 404
        else:        
            user.name = req_json.get(name)
             ...

            db.session.add(user)
            db.session.commit()
            db.session.close()
            return "", 204  # No Response
    
    def patch(self, uid: int):
        req_json = request.json
        try:
            user = User.query.filter(User.id == uid).one()
        except Exception as error:
            retrun str(error), 404
        else:
            if 'name' in req_json:
                user.name = req_json.get(name)
            ...

            db.session.add(user)
            db.session.commit()
            db.session.close()
            return "", 204  # No Response
    
    def delete(self, uid: int):
        try:
            user = User.query.filter(User.id == uid).one()
        except Exception as error:
            retrun str(error), 404
        else:
            db.session.delete(user)
            db.session.commit()
            db.session.close()
            return "", 204  # No Response


if __name__ == '__main__':  # для команды flask не нужно
    app.run(debug=True)
```

### Неймспейсы

\- используются для деленя приложения по префиксу URL.

* повышают читаемость кода
* повышают тестируемос кода

```python
book_ns = api.namespace('books')
author_ns = api.namespace('authors')

@book_ns.route('/')
class BooksView(Resource):
    ...
```

## CURL

\- это инструмент командной строки для передачи данных по сети.

```
curl -X GET 'http://127.0.0.1:5000/'
```

```
curl -X POST 'http://127.0.0.1:5000/' -H 'Content-Type: application/json' -d '{"name": "Daniil"}'
```
