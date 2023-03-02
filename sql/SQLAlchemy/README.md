# ORM

**Object Relational Mapper** - паттерн, для абстрагирования от реализации DBMS (СУБД) автоматизированно переводящий поля DB в поля класса и выполняющий SQL-запросы посредством методов класса.

**DB** $\Leftrightarrow$ **СУБД** $\Leftrightarrow$ **SQL-запросы** $\Leftrightarrow$ **ORM** $\Leftrightarrow$ **app**


## [SQLAlchemy](https://www.sqlalchemy.org/)

<img src="images/sqlalchemy.png" alt="SQLAlchemy logo" title="SQLAlchemy logo" style="height: 200px;"/>

## [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/latest/)

\- расширение для Flask, добавляющее поддержку SQLAlchemy.

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
| BOOLEAN | Boolean |
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
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # DB создасться в оперативной памяти
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Модель
class User(db.Model):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))


with app.app_context():
    db.drop_all()  # удалить все таблицы
    db.create_all()  # создать все таблицы
    
    user1 = User(id=1, name='username1')
    user2 = User(id=2, name='username2')
    
    with db.session.begin():
        # db.session.add(user1)
        db.session.add_all([user1, user2])
```


### Получение данных

```python
# users = db.session.query(User).all()
users = User.query.all()
users_count = User.query.count()

user1 = User.qury.all().first()
user1_json = json.dumps({
    'id': user.id,
    'name': user.name,
})
user2 = User.query.get(2)  # primary key
```


### Ограничения и Foreign Key

```python
class User(db.Model):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    login = db.Column(db.String(40), unique=True)
    age = db.Column(db.Integer, db.CheckConstraint('age >= 18'), default=18)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id', ondelete='SET NULL')
    
    group = db.relationship('Group')
    
    def __repl__():
        return f'<User: {self.name}>'


class Group(db.Model):
    __tablename__ = 'group'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))
    
    users = db.relationship('User')
```


### Добавление строк

```python
with app.app_context():
    user1 = User(id=1, name='username1')
    group1 = Group(id=1, name='groupname1', users=[user1])
    
    db.session.add(group1)
    db.session.commit()
    
    user2 = User(id=2, name='username2, group=group1)

    db.session.add(user2)
    db.session.commit()
    
    print(db.session.new)  # список недобавленных объектов
    db.session.commit()
    
with app.app_context():
    user_with_group = User.query.get(1)
    print(user_wuth_group.group.name)
```

***

## SQL-запросы

```sql
SELECT * FROM user WHERE age < 30
```

```python
# query = db.session.query(User).filter(User.age < 30)
query = User.query.filter(User.age < 30)
user = query.one()  # вызовет исключение, если список пустой
user_name = query.first().name
```

---

```sql
SELECT * FROM user WHERE age > 24 AND age < 30
```

```python
query = db.session.query(User).filter(User.age > 24, User.age < 30)
users = query.all()
```

---

```sql
SELECT * FROM user WHERE age < 24 OR name IS NONE
```

```python
from sqlalchemy import or_
query = db.session.query(User).filter(or_(User.age < 24, User.name == None))
users = query.all()
```

---

```python
filter(User.name.like('D%'))
filter(User.name.in_([1, 2]))
filter(User.name.notin_([1, 2]))
filter(User.name.between(1, 5))
```  

---

```sql
SELECT * FROM user LIMIT 10 OFFSET 100
```

```python
users = db.session.query(User).limit(10).offset(100).all()
```

---

```sql
SELECT * FROM user ORDER BY age DESC 
```

```python
from sqlalchemy import desc
users = db.session.query(User).order_by(User.age).all()  # ASC
users = db.session.query(User).order_by(desc(User.age)).all()
```


## Объединение таблиц

```sql
SELECT user.name, group.name AS grp_name FROM user INNER JOIN group ON user.group_id = group.id
```

```python
users = db.session.query(User.name, Group.name.label('grp_name')).join(Group).all()
```

---

```sql
SELECT user.name, group.name AS grp_name FROM user OUTER JOIN group ON user.group_id = group.id
```

```python
# users = db.session.query(User.name, Group.name.label('grp_name')).join(Group, outer=True).all()
users = db.session.query(User.name, Group.name.label('grp_name')).outerjoin(Group).all()
```

### Группировка

```sql
SELECT COUNT(group.id) AS count_1 FROM user
JOIN "group" ON "group".id = user.group_id
WHERE "group".id = 1
GROUP BY "group".id
```

```python
from sqlalchemy import func
# func.column(User.id)  - count(user.id)
query = db.session.query(func.column(User.id)).join(Group).filter(Group.id == 1).group_by(Group.id)
num = query.scalar()
```

***

## обновление данных

```python
# изменение поля
user = User.query.get(2)
user.name = 'updated_name'
db.session.add(user)
db.session.commit()

# удаление записи
user = User.query.get(2)
db.session.delete(user)
db.session.commit()
# проверка
User.query.get(2) is None   # True

# удаление группы объектов
db.session.query(User).filter(User.age < 30).delete()
db.session.commit()
# проверка
db.session.query(User).filter(User.age < 30).all() == []. # True
```


## Транзакционность

фиксирование только при достижении полноценного результата
сначала делается, потом вносится в DB

```python
db.session.flush()  # если нет транзакции, то метод ничего не сделает
```

заносит все изменения в DB (INSERT, DELETE, UPDATE) но не фиксирует их

---

```python
db.session.commit()  # если нет транзакции, то метод ничего не сделает
```

.commit = .flush + фиксация

---

```python
db.session.close ()  # закрытие сессии
```

закрытие сессии

---

```python
BEGIN
...
FLUSH
COMMIT or ROLLBACK

with db.session.begin():
    ...
# no need to commit
```

### вложенная транзакция

```python
with db.session.begin():
    try:
        ...
        nested = db.session.begin_nested()
        try:
            ...
            nested.commit()
        except:
            nested.rollback()
        db.session.commit()
    except:
        db.session.rollback()
```

***

## Миграция

\- процесс изменения структуры DB. (~ ALTER TABLE)\
\- файл со списком запросов для обновления DB.

**Flask-Migrate** $\leftarrow$ **Alembic**

```
pip install Flask-Migrate
```

```python
from flask_migrate import Migrate

#
migrate = Migrate(app, db, render_as_batch=True)  # render_as_batch - настройка, чтобы sqlite3 мог удалять/добавлять колонки
```

```
flask db init
flask db migrate -m 'add user.role, group.status'  <!-- создать миграцию -->
flask db upgrade  <!-- накатить -->
flask db downgrade  <!-- откатить -->
```
