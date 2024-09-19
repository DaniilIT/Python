# Integrated Development Environment

– редактор с подсветкой кода, запуском, автодополнением, проверкой ошибок и еще сотней функций.

## PyCharm

– это интегрированная среда разработки (IDE) для Python от компании JetBrains.

### HotKeys (keyboard shortcuts)

* Double `⇧Shift` (`⌘Сmd`⁠`⇧Shift`⁠`A`) - поиск везде
* `⌥Opt`⁠`↩Enter` - показать контекстные действия
*
* `⌘Cmd`⁠`1` - переключить на Project
* `⌘Cmd`⁠`7` - переключить на Structure
* `⌘Cmd`⁠`0` (`⌘Cmd`⁠`K`) - переключить на Commit; `⌘Cmd`⁠`⇧Shift`⁠`K` - git push
* `⌘Cmd`⁠`E` - показать последние файлы; `⇧Shift`⁠`⌘Cmd`⁠`E` - код; `⌫` - удалить
*
* `⌥Opt`⁠`↑` - расширить выбор на конструкцию
* `⇧Shift`⁠`↑` - расширить выбор на строку
* `⇧Shift`⁠`⌥Opt`⁠`↓` - перенести строку; `⇧Shift`⁠`⌘Cmd`⁠`↑` - перенести блок
* `⌘Cmd`⁠`⇧Shift`⁠`-` - свернуть все блоки; `⌘Cmd`⁠`⇧Shift`⁠`=` - развернуть
* `⌘Cmd`⁠`D` - дублировать строку
* `⌘Cmd`⁠`⌫Del` - удалить текущую строку
*
* `⌥Opt`⁠`⌘Cmd`⁠`L` - форматировать код; `⇧Shift`⁠`⌥Opt`⁠`⌘Cmd`⁠`L` - настройки
* `⌘Cmd`⁠`/` - закомментировать код
* `⌥Opt`⁠`Space` - показать код функции
* `⌘Cmd`⁠`B` (`⌘Cmd`⁠`ЛКМ`) - перейти к объявлению функции и найти использования
* `^Ctrl`⁠`⌥Opt`⁠`F7` - подробный поиск использования
* `⌘Cmd`⁠`P` - показать сигнатуру аргументов
*
* `^Ctrl`⁠`R` - запуск кода
* `⌥Opt`⁠`⌘Cmd`⁠`R` - перейти к следующему breakpoint
* `⌥Opt`⁠`⌘Cmd`⁠`T` - обернуть код выражением
* `fn`⁠`^Ctrl`⁠`Space` - показать допустимые методы
* `fn`⁠`⇧Shift`⁠`F6` - переименовать переменную везде
* `⌥Opt`⁠`⌘Cmd`⁠`V` (`⌥Opt`⁠`⌘Cmd`⁠`M`) - извлечь переменную (метод) везде


## Visual Studio Code

– легкий, но мощный редактор кода.
(Visual Studio - отдельный IDE, оба от MicroSoft)

Плагины:
* ms-python, python
* ms-azuretools.vscode-docker
* ms-vscode-remote.remote-ssh
* njpwerner.autodocstring
* LittleFoxTeam.vscode-python-test-adapter
* Natizyskunk.sftp
* mjqdev.vscode-python-typehint
* eamodio.gitlens

```shell
code .  # открыть VSCode в текущей директории
```

### Горячие клавиши

* `⌘Cmd`⁠`.` – добавить import (в PyCharm `⌥Opt`⁠`↩Enter`)
* `⌘Cmd`⁠`ЛКМ` – просмотр исходного кода
* `fn`⁠`F2` – переименовать переменную внутри блока
*
* `^Ctrl`⁠`⇧Shift`⁠`R` - запуск
* `⌥Opt`⁠`⌘Cmd`⁠`L` - авто PEP8
* `⇧Shift`⁠`⌘Cmd`⁠`U` - инвертировать регистр
*
* `⇧Shift`⁠`^Ctrl`⁠`~` – открыть терминал

`запуск` -> `отладка` -> `lounch.json` / `Python: Select Intepreter`

`тесты` -> `configure` -> `pytest` -> `tests`

### Разработка на удаленной машине по ssh tunnel

`⌘Сmd`⁠`⇧Shift`⁠`P` – открыть палитру команд

> Remote-SSH: Connect to Host... –> выбрать хост

sftp.json:
```json
{
    "name": "ProjectName_server",
    "host": "<IP4>",
    "protocol": "sftp",
    "port": 22,
    "username": "dmanujlov",
    "remotePath": "/home/dmanujlov/ProjectName",
    "uploadOnSave": false,
    "useTempFile": true,
    "openSsh": true,
    "agent": "$SSH_AUTH_SOCK",
    "privateKeyPath": "~/.ssh/key",
    "passphrase": false
}
```

В .gitignore добавить `!.vscode/sftp.json`

Чтобы обновить файлы, необходимо выделить их и выбрать `Upload File`
