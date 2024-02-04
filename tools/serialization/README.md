## Сериализация 

– процесс преобразования структуры данных в последовательность битов.

### JSON

– это формат сериализации в текстовый формат.

```python
import json, pickle
from sys import stderr

def upload_json(json_path):
    json_content = []
    try:
        with open(json_path, 'r', encoding='utf-8') as json_file:
            json_content = json.load(json_file)
    except FileNotFoundError:
        stderr.write(f"failed to find {json_path}.\n")
    except json.JSONDecodeError:  # pickle.UnpicklingError
        stderr.write(f"failed to decode {json_path}.\n")
    return json_content

def download_json(json_path, json_content):
    with open(json_path, 'w') as json_file:
        json.dump(json_content, json_file, indent=2, ensure_ascii=False)
```

Типы данных:
* строка (только двойные кавычки)
* число
* объект JSON
* массив
* boolean (true, false)
* null

Если нужно передать другие типы данных, то вместо json используется `pickle`,
который сериализует в бинарный формат.


### [marshmallow](https://marshmallow.readthedocs.io/en/stable/index.html)

– независимая от ORM/ODM фреймворка библиотека для сериализации сложных структур.

```
pip install marshmallow
```

типы полей: Bool, Int, Decimal, Float, DataTime, Str, Email [и т. д.](https://marshmallow.readthedocs.io/en/stable/_modules/marshmallow/fields.html)

```python
from marshmallow import Schema, fields

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    age = db.Column(db.Integer)

# Схема - описание полей сложной структуры.
class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    age = fields.Int()

user1 = User(name="A", age=18)
user2 = User(name="B", age=30)

user_schema = UserSchema()
user_dict = user_schema.dump(user1)
user_json = user_schema.dumps(user1)

users_schema = UserSchema(many=True)
users_list = user_schema.dump([user1, user2])
users_json = user_schema.dumps([user1, user2])

s = '{"name": "C", "age": 26}'
user_dict = user_schema.loads(s)
user = User(**user_dict)
```

### [Dataclass](https://skyengpublic.notion.site/24-2-d74cb76282624e4d8d4288f4a5940903)

– описание структур данных

```python
from typing import Optional
from dataclasses import dataclass, field

@dataclass
class Person:
    first_name: str
    last_name: str = ''
    age: Optional[int] = None
    children: list[str] = field(default_factory=list)

Person(first_name='Daniil', age='27')
```

```python
from dataclasses import dataclass, field
import marshmallow
import marshmallow_dataclass

@dataclass
class Person:
    name: str
    last_name: str = field(metadata={'data_key': 'lastName'})
    age: int

    class Meta:
        unknown = marshmallow.EXCLUDE  # marshmallow.exceptions.ValidationError
 
PersonSchema = marshmallow_dataclass.class_schema(Person)
PersonSchema().load({'name': 'alex', 'lastName': '', 'age': '100', 'ds': 123})
```


### prettytable

```python
import prettytable as pt

my_table = pt.PrettyTable()
my_table.max_width = 40

columns = ['id', 'col_1', 'col_2']
my_table.field_names = columns

rows = [
  (1, 'A', True),
  (2, 'B', True),
  (3, 'C', False),
]
my_table.add_rows(rows)
my_table.add_row((4, 'D', True))

print('my_table:')
print(my_table)
```

```
my_table:
+----+-------+-------+
| id | col_1 | col_2 |
+----+-------+-------+
| 1  |   A   |  True |
| 2  |   B   |  True |
| 3  |   C   | False |
| 4  |   D   |  True |
+----+-------+-------+
```

Кодирование:
```
poetry add ansible-vault-win
ansible-vault encrypt deploy/.env --output deploy/vault.env
ansible-vault decrypt deploy/vault.env
```
