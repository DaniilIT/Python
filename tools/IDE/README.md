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
code .  # отекрытие VSCode
```

`cmd + .` – добавить в import (в PyCharm `alt + enter`) \
`cmd + ЛКМ` – просмотр исходного кода \
`fn + F2` – переименовать переменную внутри блока

`shift + ctrl + ~` – открыть терминал

`запуск` -> `отладка` -> `lounch.json` / `Python: Select Intepreter`

`тесты` -> `configure` -> `pytest` -> `tests`

### Разработка на удаленной машине по ssh tunnel

`shift + cmd + P` – открыть палитру команд

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


## Integrated Development Environment

– интегрированная среда разработки - редактор с подсветвой кода, запуском, автодополнением, проверкой ошибок и еще сотней функций.

`ctrl + shift + R` - запуск\
`alt + cmd + L` - авто PEP8\
`shift + cmd + U` - инвертировать регист
