# Tools

## Терминал *(консоль)*

– текстовый интерфейс для работы с операционной системой.

`ctrl + alt + T` *(linux)* – hot key для запуска терминала

```sh
sudo apt update && sudo apt upgrade  # apt-get – явное управления пакетами
pip install --upgrade pip
```

`Tab` – автозавершение имен\
`ctrl + C` – завершение процесса\
`ctrl + D` – **exit()** завершение python

**cwd** – *current work directory*\
**pwd** – напечатать путь к cwd *(**cd** без аргументов для windows)*

**cd** – переместиться в катало&#x301;г
* **~** переместиться в домашнюю директорию (по умолчанию)
* **..** переместиться на уровень выше
* **-** вернуться назад

**ls** – показать содержимое *cwd* *(**la** с опциями ниже)* *(**dir** для windows)*
* **-l** показать в подробном формате (- or d)(r4w2x1 – ugo)
* **-a** показать скрытые файлы

**tree** – показать иерархию файлов

```sh
chmod a+x <file>  # изменить permissions: сделать файл исполняемым для всех
chmod 644 <file>  # 600 для private ключа и 755 для каталога
```

**man** – *manual* посмотреть руководство по команде\
**history** – посмотреть историю команд\
**sudo** – выполнить команду от имени суперпользователя *(root)*\
**clear** – очистить экран

`ctrl + H` *(linux)* `shift + cmd + .` *(mac)* – отобразить скрытые файлы

**cp** – копировать (и вставить в новое место)\
**mv** – переместить (и переименовать)\
**mkdir** – создать папку\
**rmdir** – удалить пустую папку *(**rd** для windows)*\
**touch** – создать файл\
**rm** – удалить файл *(**del** для windows)*
* **\*** удалить все файлы
* **-rf** удалить папку со всем содержимым

**>** – записать в файл\
**>>** – не перезаписать, а добавить
```sh
echo 'Hi' > file.txt
```

**cat** – прочитать содержимое файла\
**head** – прочитать первые 10 строк\
**tail -n 2** – прочитать последние 2-е строки

`f` – *forward* показать следующую страницу\
`b` – *backward* показать предыдущую страницу\
`q` – *quit* выход из режима просмотра\

**grep** – поиск *(**findstr** для windows)*
```sh
grep -i word file.txt  # поиск по файлу с игнорированием регистра
cat file.txt | grep word -n  # поиск по файлу и вывести номера строк
```

~~Less~~, Nano, Emacs, **Vim** – текстовое редакторы\
`ctrl + X` – выйти из nano\
`I` – режим ввода\
`ctrl + [` – командный режим\
**:q!** выйти без сохрaнения\
**:wq** выйти с сохранением

Переменные окружения:
```sh
export EDITOR=vim
echo $EDITOR
unset EDITOR
set -a && source .env && set +a
```


## Core libraries

### os

```python
import os

print(os.getenv('HOME'))  # переменная среды
print(os.environ.get('HOME'))  # '/Users/daniil'
os.environ['USER'] = 'daniil'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
print(os.getcwd())  # путь к текущей директории
dir_contents = os.listdir('./data')  # содержимое директории
os.chdir('..')  # перейти в директорию

if os.path.isdir(...):  # проверка на директорию
if os.path.isfile(...):  # проверка на файл

file_path = './img.png'
if not os.path.exists(file_path): # проверка существования
    with open(file_path, 'x'):  # создать файл
        pass
os.remove(file_path)  # удалить файл
os.replace('img.png', 'imgs/img.png')  # переместить
os.rename('img.png', 'pic.png')  # переименовать
os.mkdir('./imgs')  # создать папку
os.makedirs('.data/imgs', exist_ok=True)  # создать цепочку папок
os.rmdir('.data/imgs')  # удалить пустую папку

file_path = './imgs/pic.png'
f_dir = os.path.dirname(file_path)  # ./imgs
f_name = os.path.basename(file_path)  # pic.png
f_dir, f_name = os.path.split(file_path)
file_path = os.path.join(f_dir, f_name)
f_extension = os.path.splitext(f_name)[1]  # .png
```

### pathlib

```python
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
print(Path.cwd())  # показать путь к текущей директории
dir_contents = [*Path('./data').iterdir()]  # содержимое директории

Path.touch('test.txt', exist_ok=True)  # создать файл
Path.unlink('test.txt')  # удалить файл
Path.replace(...)  # переместить
Path.rename(...)  # переименовать
Path.mkdir('.data/imgs', exist_ok=True)  # создать директорию
Path.rmdir('./imgs')  # удалить директорию

path = Path('./data', 'imgs', 'pic.png')
f_dir = path.parent  # data/imgs
f_name = path.name  # pic.png
f_dir.joinpath(f_name) or f_dir / f_name  # data/imgs/pic.png
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
import sys

sys.stderr.write(f'Соединение с сервером прервано.\n')  # поток ошибок
print(sys.argv)  # список аргументов (0 - имя исполняемого скрипта)
sys.exit(0)  # выход из python
```

### logging

Логирование – записи действий, вызванных пользователями.

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

**Переменные окружения** – это набор пар ключ-значение для пользовательской среды.

```sh
pip install python-dotenv
```

```python
import os
from dotenv import dotenv_values, load_dotenv

token = dotenv_values('.env')['TOKEN']

load_dotenv('.env', oveгride=True)
token = os.getenv('TOKEN')
```
