## Терминал

\- текстовый интерфейс для работы с операционной системой.

**cwd** - current work directory\
**pwd** - показать путь к cwd (*cd* для windows)
```
> /Users/daniil/Documents/Learning/Python
```

**man** - посмотреть руководство (manual) к команде\
**sudo** - выполнить команду от имени суперпользователя\
**clear** - очистить экран

`Tab` - автозавершение имен\
`f` - forward показать следующую страницу\
`b` - backward показать предыдущую страницу\
`q` - выход из режима просмотра\
`ctrl + c` - завершение процесса ('exit()')

**ls** - показать содержимое cwd (*dir* для windows)
* **-l** показать в длинной формате
* **-R** показать все файлы в папках
* **-a** показать скрытые файлы

**cd** - переместиться в каталог
* **..** переместиться на уровень выше
* **-** вернуться назад
* **~** переместиться в домашнюю директорию

**mkdir** - создать директорию\
**rmdir** - удалить директорию (*rd* для windows)\
**touch** - создать файл\
**rm** - удалить файл (* - удалить все файлы) (*del* для windows)\
**cp** - копировать (и вставить в новое место)\
**mv** - переместить или переименовать

'>' - output вывести не в терминал, а записать в файл\
'>>' - не перезаписать, а добавить
```
echo 'Hi' > file.txt
```

**open** - открыть файл\
**cat** - показать содержимое файла\
**head** - показать первые 10 строк\
**tail -n 2** - показать последние 2-е строки

**less** пейджер - чтение файлов\
**Grep** - поиск\
Например: *ls | grep .txt* или *grep -n 'word' text.txt* (выведутся строки и их номера) *-i* (игнорировать регистр)
**Nano, Emacs, Vim** - редактирование файлов

`i` - режим ввода\
`ctrl + [` - режим ввода\
`:` - режим командной строки

'q!' выйти без сохрaнения\
':w' сохранить\
':wq' выйти с сохранением


### os

```python
import os

print(os.getenv('HOME'))  # переменные среды
print(os.environ.get('HOME'))  # '/Users/daniil'
os.environ['USER'] = 'Daniil'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
print(os.getcwd())  # показать путь к текущей директории
os.listdir('./data')  # показать содержимое cwd
os.chdir('..')  # перейти в директорию

if os.path.exists('./data'):  # проверка существования
if os.path.isdir():  # проверка на директорию
if os.path.isfile():  # проверка на файл
        
os.mkdir('./imgs')  # создать директорию
os.makedirs('.data/imgs', exist_ok=True)  # создать цепочку
os.rmdir('./imgs')  # удалить пустую директорию
os.remove('test.txt')  # удалить файл
os.replace(...)  # переместить
os.rename(...)  # переименовать

path = './data/imgs/pic.png'
base = os.path.basename(path)  # pic.png
dst = os.path.dirname(path)  # ./data/imgs
os.path.split(path)  # ('./data/imgs', 'pic.png')
os.path.join(dir_, base)  # ./data/imgs/pic.png
print(os.splitext(path)[1])  # .png
```


### pathlib

```python
from pathlib import Path

print(Path.cwd())  # показать путь к текущей директории
Path.iterdir('./data')  # показать содержимое cwd
        
Path.mkdir(exist_ok=True)  # создать директорию
Path.rmdir('./imgs')  # удалить директорию
Path.unlink('test.txt')  # удалить файл
Path.replace(...)  # переместить
Path.replace(...)  # переименовать

path = Path('./data', 'imgs', 'pic.png')
base = path.name  # pic.png
dst = path.parent  # data/imgs
dst.joinpath(base)  # data/imgs/pic.png
print(path.suffix)  # .png
```


### pathvalidate

```python
from pathvalidate import sanitize_filename, sanitize_filepath

file_name = sanitize_filename('fi:l*e/pa?t>h|.t<xt')  # filepath.txt
file_path = sanitize_filepath('fi:l*e/pa?t>h|.t<xt')  # file/path.txt
```


### sys

```python
from sys import stderr
stderr.write(f"Соединение с сервером прервано.\n")  # поток ошибок

print(sys.argv)  # список аргументов (0 - имя исполняемого скрипта)
sys.exit(0)  # выход из python
```


### logging

```python
import logging
logging.basicConfig(filename='app.log', filemode='w', level=logging.INFO,
                    format='%(process)d - %(levelname)s - %(asctime) - %(message)', datefmt='%d-%b-%y %H:%M:%S')
logging.warning('Соединение с сервером прервано.')
logging.error('Сервер упал.')
```

- DEBAG
- INFO
- <u>WARNING</u>
- ERROR
- CRITICAL


### argparse

```python
import argparse

def create_parser():
    """Функция производит синтаксический анализ командной строки
    """
    parser = argparse.ArgumentParser(
        description='Программа'
    )
    parser.add_argument(
        'dest_folder',
        help='Путь к каталогу',
    )
    parser.add_argument(
        '-p',
        '--page',
        help='Номер страницы',
        default=1,
        type=int,
    )
    parser.add_argument(
        '--skip',
        help='Флаг',
        action='store_true',
    )
    return parser

args = create_parser().parse_args()
print(args.page)
```


### dotenv

**Переменные окружения** — это набор пар ключ-значение для пользовательской среды.

```
pip install python-dotenv
```

```python
TOKEN=secret
```

```python
from dotenv import dotenv_values

token = dotenv_values('.env')['TOKEN']
```

```python
import os
from dotenv import load_dotenv

load_dotenv(oveгride=True)
token = os.getenv('TOKEN')
```


## with

\- менеджер контекста

включает в себя dunder методы: __enter__ и __exit__, заменяет try, except и **close()** в finally.

```python
with open(file_path, 'w') as file:
    file.write(text)
    
# 'a' -  дописать в конец
# 'b' -  бинарный режим

with open(file_path, 'r') as file:
    for line in file:
        print(line.rstrip())
```


## Сериализация 

\- процесс преобразования структуры данных в последовательность битов.

### json

```python
import json
from sys import stderr


def upload_json(json_path):
    json_content = []
    try:
        with open(json_path, 'r', encoding='utf-8') as json_file:
            json_content = json.load(json_file)
    except FileNotFoundError:
        stderr.write(f"failed to find {json_path}.\n")
    except json.JSONDecodeError:
        stderr.write(f"failed to decode {json_path}.\n")
    return json_content


def download_json(json_path, json_content):
    with open(json_path, 'w') as json_file:
        json.dump(json_content, json_file, indent=2, ensure_ascii=False)
```

### [marshmallow](https://marshmallow.readthedocs.io/en/stable/index.html)

\- независимая от ORM/ODM фреймворка библиотека для сериализации сложных структур.

```
pip install marshmallow
```

типы полей: Bool, Int, Decimal (число с фиксированной точностью), Float, DataTime, Str, Email и т. д.

```python
from marshmallow import Schema, fields

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    age = db.Column(db.Integer)

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


### IDE

\- интегрированная среда разработки - редактор с подсветвой кода, запуском, автодополнением, проверкой ошибок и еще сотней функций.

`ctrl + shift + R` - запуск\
`alt + cmd + L` - авто PEP8
