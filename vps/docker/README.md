# Docker

\- это платформа для разработки и запуска контейнеров, которая позволяет запускать несколько изолированнх приложений внутри одной виртуальной машины.

<img src="images/docker.webp" alt="docker" title="docker" style="height: 240px;"/>


## Контейнеризация

позволяет запускать процессы в изолированном окружении внутри ОС.

**Контейнер** - это набор запущенных процессов, находящийся внутри собственного окружения.

В ядре **Linux** для изоляции есть два инструмента:

* **namespaces** - это абстракция над ресурсами в ОС. В настоящее время существует семь типов пространств имен: Cgroups, IPC, Network, Mount (файлы и каталоги), PID, User, UTS.
* **Cgroups** - отвечает за управление потреблением ресурсов.

### отличия от VM

* VM использует гипервизор (ПО для запуска VM), который создает отдельные ОС выделяя им конкретную долю ресурсов.
* Докер (кистема контейнеризации) использует инструменты основной ОС (без процесса виртуализации)

### Архитектура

- Docker daemon - (фоновый процесс) сервис, который осуществляет всё взаимодействие с контейнерами.
- Docker client - интерфейс командной строки для управления Docker daemon.


## основный понятия
 
 * **Docker image (образ)** - неизменяемый файл, из которого разворачиваются контейнеры.
 
```bash
docker images  :: показать локальные образы
docker pull <img>  :: скачать образ из репозитория
docker rmi <img> :: удалить образ
```

* **Docker Registry** - хранилище с докер-образами. Чтобы каждый раз не собирать образ, его можно отправить в репозиторий, например Docker Hub. Платные - Docker Registry, Nexus, Harbor, Artifactory.

* **Dockerfile** - инмтрукция для сборки образа. Текстовый файл с командами, в котором указаны все зависимости.

```Docker
# ./docker
From python:3

RUN apt update && apt -y install gettext-base
WORKDIR /code
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

CMD ["python", "./main.py"]  # ./run.sh
```

создать образ из Dockerfile:
```bash
docker build -t my_image .
```

* **FROM** - базовый образ
* **RUN** - выполнить команду
* **WORKDIR** - сменить базовую директорию
* **ENV** - пробросить переменные окружения
* **ARG** - параметры сборки
* **COPY** - копирование файлов
* **CMD** -  команда при старте контейнера

```
# ./docker
FROM ubuntu:20.04
RUN apt update && apt install -y nginx
CMD nginx -g 'deamon off;'
```


## Контейнеры

Запуск контейнера:
```bash
docker run my_image
docker run -p 8080:80 my_image  :: переброс портов
docker run docker/getting-started  :: обучающий веб-сервис
docker run -d nginx  :: запуск в фоновом режиме
docker run nginx:1.20  :: зауск конкретной версии веб-сервиса для раздачи статики
```

 в этот момент
* инициализируется файловая система
* выдается IP-адрес внутри сети докера
* запускается команда `CMD` из Dockerfile и ей выдается PID 1

```bash
docker ps  :: посмотреть запущенные процессы
docker ps -a  :: посмотреть и остановленные процессы
docker logs <id / name>  :: посмотреть логи приложения
docker rm <id>  :: остановить приложение
docker rm -f <id>  :: даже работающее
docker system prune  :: удалить остановленные приложения из ps -a
```

## Сеть

**bridge** - сетевой мост (docker0) для доступа в Интернет. Для каждого контейнера создается свой виртуальный сетевой интерфейс.\
**host** - подключение происходит к сети через сетевое пространство машины.\
**none** - нет сети.

Создание сети:
```bash
docker network ls  :: посмотреть созданные сети
docker network inspect <сеть>  :: детальная информация
docker network create <сеть>  :: создать

docker run --network=<сеть> <img>
```

## Файловая система

Образ состоит из слоев. **Слой** - добавление файлов поверх предыдущего слоя. Первый слой - базовый scratch.

```Docker
# ./docker
FROM python:3.10-slim

WORKDIR /code
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app.py .
COPY migrations migrations
COPY docker_config.py default_config.py

CMD flask run -h 0.0.0.0 -p 80
```

### Запуск PosgreSQL

```python
# ./docker_config.py
SQLALCHEMY_DATABASE_URL = 'postgresql://flask_app:password@pg/flask_app'
```

Запуск двух контейнеров в одной сети:
```bash
docker run --name postgres  :: название контейнера
	-e POSTGRES_USER=flask_app  # прокинуть переменные окружения внутрь
	-e POSTGRES_PASSWORD=password
	-e POSTGRES_DB=flask-app
	--network=flask_app
	--network-alias pg
	-v $(pwd)/pg_data:/var/lib/postgresql/data  :: volume
	-d postgres <key>  :: запустить в фоновом режиме

docker run --network flask_app -p 8000:80 --name flask-app -d flask-app
```

```bash
docker exec flask-app ls  :: посмотреть файлы в контейнере
docker exec -it flask-app /bin/bash  :: подключиться внутрь к контейнеру
root $ > apt upgrate
root $ > apt install procps
root $ > ps aux
root $ > kill <PID>
root $ > flask db upgrade  :: применение миграций
```

## Команды

```bash
curl -I localhost:80  :: показадь headers
```

```bash
ps aux  :: показать запущенные процессы
top  :: интерактивная консоль всех текущих процессов в системе
htop  :: запущенные в системе процессы

dig sky.pro  :: узнать IP-адрес sky.pro
dig MX sky.pro  :: узнать почтовые адреса sky.pro
netstat -tulpn. :: активные порты
aptitude search packet-name  :: поиск пакета packet-name

add-apt-repository ppa:deadsnakes/ppa  :: установить python в ubuntu
apt install python-pip  :: to install pip

apt install net-tools
ifconfig  :: посмотреть IP адреса кофига

apt install dnsutils
host <alias_name>  :: показать IP по доменному имени

journalctl -u app_name  :: показать системные log для app_name
journalctl -u app_name -f  -n 1000  :: последние

sudo lsof -i :5000
kill 7426

#копирование файлов
scp -r dir stasy23@51.250.27.163:python_3/

#старт приложения
systemctl start unit_name
systemctl stop unit_name
systemctl daemon-reload

systemctl enable unit_name  :: на следующей перезагрузке
systemctl disable unit_name

etc/ssh/sshd_config  :: системные настройки
sudo service ssh start  :: обновить системы настройки

python3.10 -m venv env
virtualenv env
. env/bin/activate

rm -r dir  :: удалить непустой каталог

usermod -aG sudo username  :: дать права администратора пользователю
```

***

## Docker volumes

\- инструмент для хранения файлов в директории `var/lib/docker/volumes`, такой слой, который выделяется контейнеру, и не удаляется после удаления контейнера.

**Монтирование директории с хоста - пробросить внутрь папку на компьютере

Stateless файлы хранятся в  `var/lib/docker/overlay/<id слоя>`, и удаляются при завершении контейнера (эфимерность).

```bash
docker run -it --rm busybox  :: войти внутрь контейнера и удать при завершении
docker exec -it pg /bin/bash  :: отдельно войти
docker rm -f pg  :: отдельно удалить даже работающее
```

```bash
docker inspect <id or name container>  :: узнать id слоя
```

Для поиска этой дирректории в Mac OS или Windows:
```bash
docker run -it --privileged --pid=host justincormack/nsenter1  :: с помощью привилегированного контейнера
ls /var/lib/docker/overlay/
```

В Volume можно хранить:
* данные DB
* файлы, добавляемые пользователем,
* файлы конфигурации (подменять стандартные)
* при разработке пробрасывать код внутрь контейнера

Основные команды:
```bash
docker volume ls  :: посмотреть созданные volume
docker volume create  :: создать volume
docker volume inspect <name volume>   :: детальная инфо
docker volume rm <name volume>  :: удалить
docker volume prune  :: удалить все неиспользуемые в данный момент volume

# Проброс volume в контейнер
docker volume create test
docker run -v test:/dir_in_container <образ>

# Проброс директории с хоста в контейнер
docker run -v /host_dir:/dir_in_container -d nginx
```


## Docker Compose

 \- инструмент для одновременного управления несколькими контейнерами, которые входят в состав одного приложения.
 
 В одной файле описывается весь состав приложения:
 * контейнеры
 * сети
 * volumes - тома
 * порядок запуска контейнеров
 
```
# .\docker-compose.yaml
version: "3.9"
services:  # описание контейнеров
  api:  # название контейнера
    build:
      context: .
    ports:
    - 8000:80
  postgres:
    image: postgres:latest  # готовый образ
    environment:
      POSTGRES_PASSWORD: password
      POSTGRES_DB: myapp
```
 
 Основные команды:
```
docker-compose up -d # запустить всё приложение в режиме демона
docker-compose stop
docker-compose start # запустить контейнеры
docker-compose down  # остановить контейнеры и удалить все компоненты
docker-compose build  # cобрать образы
docker-compose pull  # скачать необходимые образы
docker-compose logs  # посмотреть логи сервисов
```

### порядок запуска Docker Compose

1) запустить PostgreSQL
2) применить миграции
3) запустить приложение

`depends_on` секция позволяет указать порядок запуска сервисов по условию:
- **service_started** — просто порядок запуска;
- **service_healthy** — запустить только после того, как контейнер будет работать (пройдет healthcheck);
- **service_completed_successfully** — запустить только после того, как успешно завершится другой контейнер.

```
# .\docker-compose.yaml
version: "3.9"
services:
  api:
    build:
      context: .
    ports:
    - 8000:80
    volumes:
      - ./docker_config.py:/code/default_config.py
    depends_on:
      postgres:
        condition: service_healthy
      migrations:
        condition: service_completed_successfully
  migrations:
    build:
      context: .
    volumes:
      - ./docker_config.py:/code/default_config.py
    depends_on:
      postgres:
        condition: service_healthy
    command: flask db upgrade
  postgres:
    image: postgres:latest
    environment:
      POSTGRES_USER: flask_app
      POSTGRES_PASSWORD: password
      POSTGRES_DB: flask_app
    volumes:
      - ./postgres-data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 5s
      retries: 5
```

**healthcheck** - секция, которая определяет когда контейнер корректно запущен и готов к работе.
 
 
 ## Деплой через Docker Compose на сервер
 
 1) собрать образы
```bash
 docker build -t sermalenk/flask-app:version-1 . 
```
 2) отапрвит в Docker Hub - бесплатный registry
```bash
docker build -t sermalenk/flask-app:version-1 .
docker push sermalenk/flask-app:version-1
```
 
```
# .\docker-compose.yaml
  api:
    image: sermalenk/flask-app:version-1
  migrations:
    image: sermalenk/flask-app:version-1
  postgres:
    image: postgres:latest
```
 
 3) устанавливаем Docker на сервере
 Подключаемся через SSH к серверу. И [по иснструкции](https://docs.docker.com/engine/install/ubuntu/)
 
```bash
 sudo su
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
apt-get update
apt-get install docker-ce docker-ce-cli containerd.io

# устанавливаем docker-compose
curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose
```

4) копируем docker-compose-server.yaml на сервер
```bash
scp <путь до проекта>/docker_config.py <имя>@<адрес>:.
scp <путь до проекта>/docker-compose-server.yaml <имя>@<адрес>:docker-compose.yaml
```

5) запускаем
```bash
sudo su
docker-compose up -d
```

