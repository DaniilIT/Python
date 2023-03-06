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

def generate_token(data):
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
        func(*args, **kwargs)
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
