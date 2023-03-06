# [JWT](https://pyjwt.readthedocs.io/en/stable/)

\- JSON Web Token
\- безопасный способ передачи информации между двумя участниками.

`header.payload.signature`

* **Аутентификация**
\- процедура проверки подлинности, например: сравнение паролей;
    * Basic (login, password)
    * Token (Key)
    * OAuth 2.0 (протокол)
* **Идентификация**
\- процедура выявления идентификатора (логин пароль);
* **Авторизация**
\- предоставление клиенту прав на выполнение определенных действий;

```
pip install pyjwt
```

```python
from calendar import timegm
from datatime import datatime, timedelta
from flask import Flask, request, abort
from flask_restx import Api, Resource
import jwt

app = Flask(__name__)
api = Api(app)
user_ns = api.namespace('')

secret = 's3cR$eT'  # не изменять!
algo = 'HS256'  # алгоритм

def generate_token(data):  # в токене есть информация о пользователе
    min30 = datatime.utcnow() + timedelta(minutes=30)
    data['exp'] = timegm(min30.timetuple())
    token = jwt.encode(data, secret, algorithm=algo)
    return token

def check_token(token):
    try:
        jwt.decode(token, secret, algorithms=[algo])
        return True
    except Exception as error:
        return False

def auth_required(func):
    def wrapper(*args, **kwargs):
        if 'Authorization' not in request.headers:
            abort(401)
        
        data = request.headers['Authorization']
        token = data.split('Bearer ')[-1]
        if not check_token(token):
            abort(401)
        return func(*args, **kwargs)
    return wrapper

@user_ns.route('/users/'):
    @auth_required
    def post(self):
        return '', 201

if __name__ == '__main__':
    data = {
        'username': 'myname',
        'role': 'user',
    }
    token = generate_token(data)
    is_ok = check_token
    
    app.run(debug=True)
```


## Пароли

хранятся результаты работы **хеш функции** (например md5, SH256, SH512).

\- функция, которая **необратимо** искажает исходную строку, пулучая на выходе **хеш**.

\- искаженная строка, с псевдослучайными символами, построенная на базе другой.

**HMAC-SHA256** - hash-based message authentication code

**соль** - строка, которая добавляется перед поролем, чтобы хеш получился сложнее и его сложнее было подобрать.

**брутфорс** - грубый перебор паролей.


## refresh_token

access_token имеет непродолжительное время жизни,\
и чтобы не заставлять пользователя вводить свои данные повторно, токены обновляются с помощью одноразового refresh.


## Реализация

### модель

```python
# app/dao/model
from app.database import db

class User(db.Model):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    password = db.Column(db.String)
    role = db.Column(db.String)
```

### views

```python
# app/views/user
@user_ns.route('/<int:user_id>')
class UserView(Resource)
    @admin_required    
    def delete(self, user_id):
        auth_service.delete(user_id)
        return '', 204
```

```python
@auth_ns.route('/')
class AuthsView(Resource)
    def post(self):
        data = request.json
        
        username = data.get('username', None)
        password = data.get('password', None)
        if None in [username, password]:
            return '', 400
            
        tokens = auth_service.generate_tokens(username, passwords)
        return tokens, 201
        
    def put(self):
        data = request.json
        token = data.get('refresh_token')
        
        tokens = auth_service.approve_refresh_token(token)
        return tokens, 201
```

### service

```python
# app/services/auth
from calendar import timegm
form datatime import datatime
import jwt
from flask import request, abort
from app.helpers.constants import JWT_SECRET, JWT_ALGORITHM  # 'secret', 'HS256'
from app.service import UserService
from app.container import auth_service

class AuthService:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def generate_token(self, username, password, is_refresh=False):
        user = self.user_service.get_by_username(username)
        
        if user is None:
            raise abort(404)
        
        if not is_refresh:
            if not self.user_service.compare_passwords(user.password, password):
                abort(400)
        
        data = {
            'username': user.username,
            'role': user.role,
        }
        
        min30 = datatime.utcnow() + timedelta(minutes=30)
        data['exp'] = timegm(min30.timetuple())
        access_token = jwt.encode(data, JWT_SECRET, algorithm=JWT_ALGORITHM)
        
        days30 = datatime.utcnow() + timedelta(days=30)
        data['exp'] = timegm(days30.timetuple())
        refresh_token = jwt.encode(data, JWT_SECRET, algorithm=JWT_ALGORITHM)
        
        return {
            'access_token': access_token,
            'refresh_token': refresh_token,
        }
    
    def approve_refresh_token(self, refresh_token):
        data = jwt.decode(jwt=refresh_token, key=JWT_SECRET, algorithms=[JWT_ALGORITHM])
        username = data.get('username)
        return self.generate_tokens(username, None, is_refresh=True)

```

```python
# app/service/user
import base64
import hashlib
import hmac

from app.helpers.constants import PWD_ITERATIONS, PWD_SALT  # 10_000, b'salt'
from app.dao.user import UserDAO

class UserService:
    def __init__(self, dao: UserDAO):
        self.dao = dao

    def get_one(self, user_id):
        user = self.dao.get_one(user_id)
        return user

    def get_all(self, **args):
        users = self.dao.get_all(**args)
        return users
        
    def get_by_username(self, username):
        user = self.dao.get_by_username(username)
        return user

    def create(self, user_dict):
        user_dict['password'] = self.make_password_hash(user_dict.get('password'))
        user_id = self.dao.create(req_json)
        return user_id

    def delete(self, user_id):
        user = self.get_one(user_id)
        self.dao.delete(user)
        
    def get_hash_digest(self, password):
        return hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            PWD_SALT,
            PWD_ITERATIONS
        )  # бинарная последовательность чисел
        
    def make_password_hash(self, password):
        hash_digest = self.get_hash_digest(password)
        return base64.b64encode(hash_digest)
    
    def compare_passwords(self, password_hash, other_password) -> bool:
        return hmac.compare_digest(
            base64.b64decode(password_hash),
            self.get_hash_digest(other_password)
        )
```

### decorators

```python
# app/helpers/decorators
import jwt
from flask import request, abort
from app.helpers.constants import JWT_SECRET, JWT_ALGORITHM  # 'secret', 'HS256'

def admin_required(func):
    def wrapper(*args, **kwargs):
        if 'Authorization' not in request.headers:
            abort(401)  # Unauthorized
        
        data = request.headers['Authorization']
        token = data.split('Bearer ')[-1]
        role = None
        
        role = None
        try:
            user = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            role = user.get('role', 'user')
        except Exception as error:
            abort(401)  # Unauthorized
        
        if role != 'admin':
            abort(403)  # Forbidden
            
        return func(*args, **kwargs)
    return wrapper
```
