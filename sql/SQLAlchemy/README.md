# ORM

**Object Relational Mapper** - паттерн, для абстрагирования от реализации DBMS автоматизированно переводящий поля DB в поля класса и выполняющий SQL-запросы посредством методов класса.

**DB** $\Leftrightarrow$ **СУБД** $\Leftrightarrow$ **SQL-запросы** $\Leftrightarrow$ **ORM** $\Leftrightarrow$ **app**


## SQLAlchemy

flask-sqlalchemy - интегрирует sqlalchemy в flask.

```
pip install flask flask-sqlalchemy sqlalchemy
```


### DBAPI - драйвер

указывается при подключении

* SQLite: default
* MySQL: PyMySQL
* PostgreSQL: psycorg2
* Oracle: cx-Oracle
* MS SQL: PyODBC

**DSN** - Data Source Name - строка подключения к данным.

```
dialect+driver://username:password@hostname:port/database

sqlite:///dbname.db
mysql+pymysql://root:***@localhost/dbname
postgresql+psycorg2://localhost/dbname
oracle+cx_oraccle://root:***@localhost/dbname
mssql+pyodbc://root:***@localhost/dbname
```


### Типы данных

| **SQL** | **SQLAlchemy** |
| :---: | :---: |
| BOOLEAN I Boolean |
| INTEGER | Integer |
| NUMERIC | Numeric |
| FLOAT | Float |
| TEXT | Text |
| DATE | Date |
| DATETIME | DateTime |


## пример

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URL'] = 'sqlite:///:memory:'  # DB создасться в оперативной памяти
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Модель
class User(db.Model):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))
    
db.drop_all()  # удалить все таблицы
db.create_all()  # создать таблицу

user1 = User(id=1, name='username1')
user2 = User(id=2, name='username2')

# db.session.add(user1)
db.session.add_all([user1, user2])

print(db.session.new)  # список недобавленных объектов

db.session.commit()
```


### Получение данных

```python
users = db.session.query(User).all()
users = User.query.all()
users_count = User.query.count()

user1 = User.qury.first()
user1_json = json.dumps({
    'id': user.id,
    'name': user.name,
})
user2 = User.qury.get(2)  # primary key
```
