# Distributed Version Control System

– Распределённая система управления версиями

- контроль изменений в проектах
- организация работы команды разработчиков

GitHub, GitLab, Bitbucket – сервисы онлайн-хостинга репозиториев.

### Установка:

```shell
brew install git  # mac
sudo apt install git-all  # linux
git --version
```

### Конфигурация:

```shell
git config --list  # --global --local
git config --global user.name "Manuilov Daniil"  # user.email
git config --global core.sshCommand "ssh -i ~/.ssh/id_rsa"
git config --global init.defaultBranch "master"
```

Отключить отслеживание файлов можно в `.gitignore` \
Сгенерировать это файл можно в [gitignore.io](https://www.toptal.com/developers/gitignore) (macos, visualstudiocode, pycharm, python)
- `<dir_name>/` – папки
- `/<dir_name>/` – конкретная папка
- `*.log` – шаблон
- `!important.log` – не исключать


### Базовые команды:

```shell
git init  # создать репозиторий (.git) в working directory (WD)
git add . | <file>  # добавить файл(ы) в staging area (индекс)
git restore <file>  # удалить изменения из индекса и WD
  --staged (--cashed) # убрать изменения только из индекса
git status  # просмотр текущего состояния
  -u  # просмотр неотслеживаемых файлов
git commit -m "..."  # создать коммит
  --amend  # добавить изменения в последний коммит
```

Коммиты должны иметь короткое и осмысленное описание, 
должны быть атомарными: решать полностью одну задачу.

- `Initial commit`
- `Add <package> dependency`
- `feat:` – добавление новой функциональности
  - `implement user authentication` *– реализовать аутентификацию пользователей*
- `fix:` – исправление ошибок
  - `resolve error when saving settings` *– устранить ошибку при сохранении настроек*
- `refactor:` – рефакторинг кода
  - `optimize data processing functions` *– оптимизировать функцию обработки данных*
- `docs:` – добавление документации
  - `update README with installation instructions` *– обновить README с инструкциями по установке*
- `style:` – изменение стилевого оформления
  - `correct indentation issues` *– устранить проблемы с отступами*
- `test:` – добавление новых тестов
  - `add unit tests for my class` *– добавить модульные тесты для моего класса*
- `chore:` – изменение структуры проекта
  - `rename directory A to B` *– переименовать директорию*

### Просмотр истории:

```shell
git log <branch>
  --oneline  # в коротком формате (hash + mark)
  --graph  # просмотр связей коммитов
  --no-merges  # исключить слияния
  --grep="..." -i  # поиск совпадений (игнорируется регистр)
git diff <file>  # просмотр изменений между WD и последним коммитом
  --cashed  # просмотр изменений, внесенных в индекс
git blame <file>  # просмотр кто менял каждую строчку в файле
git show <hash>  # просмотр изменений коммита
```

### Управление коммитами:

```shell
git revert <hash>  # создать обратный коммит
git reset --hard HEAD~[n] | <hash>  # удалить последние коммиты
  --soft  # не сбрасывает индекс и WD
  --mixed  # сбрасывает индекс (по умолчанию)
  --hard  # сбрасываются индекс и WD
git rm <file>  # удалить файл из индекса и WD
  --cached  # оставить файл в WD
git stash  # спрятать изменения в тайник
  stash list  # просмотр тайника
  stash pop  # достать изменения из тайника
git clean -n  # посмотреть неотслеживаемые файлы
  -fd  # удалить неостлеживаемые файлы и директории
git filter-repo --path ./.env --invert-paths  # удалить файл из истории
```

### Управление ветками:

```shell
git branch  # просмотр существующих веток
  <branch>  # создать ветку
  -d  # удалить ветку
  -D  # удалить слитую ветку
  -m  # переименовать текущую ветку
git checkout <branch | hash>  # переключиться на ветку или коммит
  -  # вернуться назад
  -b  # создать ветку
git switch <branch>  # переключиться на ветку
  -  # вернуться назад
  -c  # создать ветку
git merge  # слияние
git rebase  # перенос коммитов
  -i HEAD~[n]  # интерактивное объединение коммитов
git sherry-pick <hash>  # подставить коммит
```

### Git-Flow

– подход к ветвлению и слиянию в репозитории GIT,
что поддерживает структуру котовой базы и облегчает совместную разработку.

### Взаимодействие с онлайн-хостингами:

```shell
git clone  # создать локальную копию репозитория
git remote add origin <url>  # привязка
  get-url origin  # просмотр url
git fetch  # извлечь изменения без применения
git pull  # извлечь изменения и применить (git fetch + git merge --ff)
git push  # выгрузка изменений
  -u origin <branch>  # указать ветку назначения
  -f  # принудительно перезаписать

git tag v1.0  # создать тэг локально
git push origin v1.0  # выгрузить тэг
```

### submodule

– это другой репозиторий, который можно использовать внутри своего проекта (выглядит как папка).

```shell
git submodule add <url>
git submodule update --remote
```

Запуск pre-commit:
```
poetry add pre-commit
pre-commit install
pre-commit sample-config > .pre-commit-config.yaml
pre-commit run -a 
```
