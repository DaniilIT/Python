# CI/CD

Continuous Integration / Delivery (непрерывная интеграция и доставка) – технология автоматизации тестирования и доставки новых модулей разрабатываемого проекта конечным пользователям.

**CI**
1) Plan – решение внедрить новую функциональность
2) Code – написание кода, ручное тестирование, отправка в систему хранения (github, gitlab, bitbucket).
3) Build – сборка (создание docker image)
4) Test – тестирование (pytest)

**CD**
1) Release – присвоение рабочей версии продукта и подготовка к развертыванию на серверах (push в registry DockerHub, Artefactory, Nexus)
2) Deploy – развертывание (pull + up) на production-серверах
3) Operate – поддержка и мониторинг, анализ пользовательского опыта

Плюсы:
* увеличение частоты релизов
* повышение надежности, т. к. настраивается автоматическое тестирование
* облегчение переездов в новую инфраструктуру


## GitHub Actions

 – система CI/CD, т. е. автоматизирует deploy. (другие: Jenkins, Travis, GitLab CI/CD, Bitbucket Pipelines) 
 
 * **Workflow** – набор jobs (скриптов), представляет из себя автоматизированный процесс, определяется файлом yaml.
* **Event** – триггер (push или таймер) на запуск workflow.
* **Job** – последовательность скриптов (actions) в workflow, которая выполняется на одном сервере (runner).
* **Action** – действия, которые описаны внутри каждого шага, пользовательская библиотека готового скрипта.
* **Runner** – исполнитель скриптов, сервер.

\# .github/workflows/actions.yaml

```yaml
name: Build and deploy action
on: [push]
jobs:
  build_and_push:
    runs-on: ubuntu-latest
    steps:
      - name: clone code 
        uses: actions/checkout@v2  # Копируем код из репозитория в runner
      - name: list dir
        run: ls -la
      - name: docker build
        run: docker {image} build -t <img> .
```

uses actions из [marketplace](https://github.com/marketplace?type=actions).


## Переменные окружения

предопределенные:
- GITHUB_RUN_ID – номер сборки.
- GITHUB_REF_NAME – название ветки в git или тега.

собственные заполняются в **secrets**.

```yaml
name: Build and deploy action
on: [push]
jobs:
  build_and_push:
    runs-on: ubuntu-latest
    steps:
      - name: clone code 
        uses: actions/checkout@v2
      # Собираем образ
      - name: docker build
        run: docker {image} build -t <login>/<repo>:$GITHUB_REF_NAME-$GITHUB_RUN_ID .
      # Отправляем образ в registry
      - name: docker login
        run: echo ${{ secrets.DOCKERHUB_TOKEN }} | docker login -u ${{ secrets.DOCKERHUB_USERNAME }} --password-stdin
      - name: docker push
        run: docker push <login>/<repo>:$GITHUB_REF_NAME-$GITHUB_RUN_ID
```

actions для работы с [docker](https://docs.docker.com/language/python/configure-ci-cd/).


### Подменять переменные окружения в файлах:

```yaml
name: Build and deploy action
on: [push]
jobs:
  build_and_push:
    ...
  deploy:
  	runs-on: ubuntu-latest
  	needs: build_and_push  # последовательность исполнения
  	env:  # переменные для замены в файлах
  		DB_USER: <user>
  		DB_PASSWORD: ${{ secrets.DB_PASSWORD }}
  		DB_NAME: ${{ vars.DB_NAME }}
  	steps:
      - name: clone code 
        uses: actions/checkout@v2
      - name: render configs
        run: |
          # export DB_PASSWORD=${{ secrets.DB_PASSWORD }}
          mkdir deploy
          cat docker_config_ci.py | envsubst > deploy/docker_config.py
          cat docker-compose_ci.yaml | envsubst > deploy/docker-compose.yaml
```

**envsubst** – утилита для подстановки значений переменных окружения

```
# docker_config_ci.py
SQLALCHEMY_DATABASE_URI = "postgresql://$DB_USER:$DB_PASSWORD@postgres/$DB_NAME"

# docker-compose_ci.yaml
image: <login>/<repo>:$GITHUB_REF_NAME-$GITHUB_RUN_ID
postgres:
  environment:
    POSTGRES_PASSWORD: $DB_PASSWORD
```

```sh
brew install gettext
export DB_PASSWORD=<password>
cat docker-compose_ci.yaml | envsubst > deploy/docker-compose.yaml
```


## Загрузка файлов на сервер

Создать нового пользователя:
```sh
sudo su
adduser deploy  # задать пароль
usermod -aG sudo deploy
# vim /etc/ssh/sshd_config
# PasswordAuthentication no -> PasswordAuthentication yes
service ssh restart
```

```yaml
name: Build and deploy action
on: [push]
jobs:
  build_and_push:
    ...
  deploy:
  	runs-on: ubuntu-latest
  	needs: build_and_push
  	env:
      ...
  	steps:
  	  - name: clone code 
        uses: actions/checkout@v2
      - name: render configs
        ...
      - name: clone files to server
        uses: appleboy/scp-action@master  # готовый action для загрузки файлов через SCP
        with:
          host: ${{ secrets.HOST }}
          username: ${{ secrets.SSH_USERNAME }}
          password: ${{ secrets.SSH_PASSWORD }}
          # Указываем, какие файлы копировать
          source: "deploy/docker-compose.yaml,deploy/docker_config.py"
          # Место на виртуальной машине, куда скопируются файлы
          target: "flask-app"
          strip_components: 1  # убрать подкатолог "deploy"
      - name: run docker-compose
        uses: appleboy/ssh-action@master  # готовый action для выполнения команд через SSH
        with:
          host: ${{ secrets.HOST }}
          username: ${{ secrets.SSH_USERNAME }}
          password: ${{ secrets.SSH_PASSWORD }}
          script: |
            cd flask-app
            echo ${{ secrets.SSH_PASSWORD }} | sudo -S docker-compose up -d
```
