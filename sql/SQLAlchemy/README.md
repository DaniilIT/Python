# ORM

**Object Relational Mapper** – объектно реляционное отображение, технология программирования, которая связывает базы даннх с концепциями ООП, что позволяет абстрагироваться от реализации DBMS (СУБД) и автоматизированно отобразить поля DB в поля класса, а SQL-запросы в методы класса.


**DB** $\Leftrightarrow$ **СУБД** $\Leftrightarrow$ **SQL-запросы** $\Leftrightarrow$ **ORM** $\Leftrightarrow$ **app**


## [SQLAlchemy](https://www.sqlalchemy.org/)

<img src="images/sqlalchemy.png" alt="SQLAlchemy logo" title="SQLAlchemy logo" style="height: 160px;"/>

## [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/latest/)

– расширение для Flask, добавляющее поддержку SQLAlchemy.

```sh
python -m pip install flask flask-sqlalchemy sqlalchemy
```


### DBAPI - драйвер

указывается при подключении

* SQLite: default
* MySQL: PyMySQL
* PostgreSQL: psycorg2
* Oracle: cx-Oracle
* MS SQL: PyODBC

**DSN** - Data Source Name – строка подключения к данным.

```
dialect+driver://username:password@hostname:port/database

sqlite:///dbname.db (sqlite:///:memory:)
mysql+pymysql://root:***@localhost/dbname
postgresql+psycopg2://root:***@localhost:5432/dbname
oracle+cx_oraccle://root:***@localhost/dbname
mysql+mysqlconnector://root:***@localhost/dbname
mssql+pyodbc://root:***@localhost/dbname  # работает с разными DB
```

Для psycopg2 необходимо `brew install postgresql`,  `apt update && apt install libpq-dev` или `poetry add psycopg2-binary`


### [Типы данных](https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html#mapped-column-derives-the-datatype-and-nullability-from-the-mapped-annotation)


## пример

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # DB создасться в оперативной памяти
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # отключение сигналов об изменениях
app.config['SQLALCHEMY_ECHO'] = True  # логирование запросов

db = SQLAlchemy(app)
# db.init_app(app)

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
    
    try:
        db.session.add(user1)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
    fynally:
        db.session.close()
    
    with db.session.begin():
        db.session.add_all([user1, user2])
```

чистый sqlalchemy:
```python
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(40))

engine = create_engine('postgresql+psycopg2://postgres:postgres@localhost:5432/postgres', echo=True)  # логирование
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(engine)  # создание таблиц в случае не соответствия их с моделями
Session = sessionmaker(engine)
session = Session()
session.add(User(id=1, name='username1'))
session.commit()
```


### Получение данных

```python
# with app.app_context():
# users = db.session.query(User).all()
users = User.query.all()
users_count = User.query.count()

user1 = User.query.all().first()
user1_json = json.dumps({
    'id': user.id,
    'name': user.name,
})
user2 = User.query.get(2)  # primary key
# user2 = db.session.get(User, 2)
# user2 = User.query.filter(User.id == 2).first()  # тоже самое
# user2 = User.query.filter(User.id == 2).one()  # вызовет except, если нет объекта или объектов несколько
```

```python
import prettytable

session = db.session()
cursor = session.execute(f'SELECT * FROM {User.__tablename__}').cursor
my_table = prettytable.from_db_cursor(cursor)
my_table.max_width = 30
```


### Ограничения и Foreign Key

```python
class User(db.Model):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)  # поумолчанию True (может быть пустым)
    login = db.Column(db.String(40), unique=True)
    age = db.Column(db.Integer, db.CheckConstraint('age >= 18'), default=18)
    updated = db.Column(db.DateTime, onupdate=datetime.utcnow)
    
    group_id = db.Column(db.Integer, db.ForeignKey('group.id', ondelete='SET NULL'))
    group = db.relationship('Group')
    
    # from sqlalchemy.orm import relationship
    # group_id = Column(Integer, ForeignKey('group.id', ondelete='CASCADE'), nullable=False)
    # group = relationship('Group', back_populates='users')
    
    def __repl__():
        return f'<User: {self.name}>'


class Group(db.Model):
    __tablename__ = 'group'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))
    
    users = db.relationship('User')
    # users = relationship('User', back_populates='group')
    # users = relationship('User', backref='group', lazy=True)  # тогда только здесь указывается
    # lazy=True - загрузка данных за один раз с помощью оператора select
    # lazy=False - загрузка данных в том же запросе с помощью оператора join
    # lazy='dynamic' - возвращает query для дальнейшей обработки
```


### ManyToMany

```python
post_tags = db.Table(
    'post_tags',
    db.Column('post_id', db.Integer, db.ForeignKey('post.id', ondelete='CASCADE'), nullable=False),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id', ondelete='CASCADE'), nullable=False)
)
# post_tags = Table(
#     'post_tags', Base.metadata,
#     Column('post_id', Integer, ForeignKey('post.id', ondelete='CASCADE'), nullable=False),
#     Column('tag_id', Integer, ForeignKey('tag.id', ondelete='CASCADE'), nullable=False)
# )

					
# >>> with app.app_context():
# ...     tag1 = Tag.query.first()
# ...     post1 = Post.query.filter(Post.id==1).first()
# ...     post1.tags.append(tag1)
# ...     db.session.commit()
# >>> with app.app_context():
# ...     post1 = Post.query.filter(Post.id==1).first()
# ...     print(post1.tags)  # [<Tag id: 1>]
# >>> with app.app_context():
# ...     tag1 = Tag.query.first()
# ...     print(tag1.posts.all())  # [<Post id: 1>]

class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	tags = db.relationship('Tag', secondary=post_tags, backref=db.backref('posts', lazy='dynamic'))  # Возможно ошибка в скобках
    # tags = relationship('Tag', secondary=post_tags, back_populates='posts', lazy=True)

class Tag(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	# posts = relationship('Post', secondary=post_tags, back_populates='tags', lazy=True)
```


### Добавление строк

```python
with app.app_context():
    user1 = User(id=1, ...')
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
    print(user_with_group.group.name)
```

***

## SQL-запросы

```sql
SELECT * FROM user WHERE age < 30
```

```python
# query = db.session.query(User).filter(User.age == 18)
# query = db.session.query(User).filter_by(User.age=18)
query = User.query.filter(User.age < 30)
# print(query)  # получить сырой текст запроса
users = query.all()
user1_name = query.first().name
```

```python
stmt = select(Book).where(Book.title == 'Робинзон Крузо')
for book in session.scalars(stmt):
    print(book)
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
# posts = Post.query.filter(Post.title.contains(q) | Post.body.contains(q))
users = query.all()
```

---

```python
filter(User.name.like('D%'))  # ilike
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
# posts = Post.query.order_by(Post.created.desc()).all()
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
SELECT group.name, COUNT(user.group_id) AS count FROM "group"
OUTER JOIN "user" ON "group".id = "user".group_id
GROUP BY "group".name
```

```python
# count, sum, ...
db.session.query(Group.name, db.func.count(User.group_id)).outerjoin(User, Group.id == User.group_id).group_by(Group.name).all()
# [(_,_), (_,_), ...]
```

---



```sql
SELECT COUNT(group.id) AS count_1 FROM user
JOIN "group" ON "group".id = user.group_id
WHERE "group".id = 1
GROUP BY "group".id
```

```python
from sqlalchemy import func
# func.column(User.id) – count(user.id)
# func.lower(Student.name)
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

## Миграции

– процесс изменения структуры DB. (~ ALTER TABLE)\
– файл со списком запросов для обновления DB.

**Alembic** $\rightarrow$ **Flask-Migrate**

```sh
python -m pip install flask-migrate
```

```python
from flask_migrate import Migrate

migrate = Migrate(app, db, render_as_batch=True)  # render_as_batch - настройка, чтобы sqlite3 мог удалять/добавлять колонки
```

```sh
flask db init
flask db migrate -m 'add user.role, group.status'  # создать миграцию
# если flask не видит модели, то можно импортировать их в `/migrations/env.py`
flask db upgrade  # накатить
flask db downgrade  <!-- откатить -->
```
