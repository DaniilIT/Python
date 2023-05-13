# Docker

– это ПО для управления контейнерами, которое позволяет запускать несколько изолированнх приложений внутри одной виртуальной машины.\
Запускается на Linux (или эмулирует её))

<img src="images/docker.webp" alt="docker" title="docker" style="height: 240px;"/>


## Контейнеризация

**Контейнер** – это приложение (набор запущенных процессов), которое изолировано от всех остальных.

В ядре **Linux** для изоляции есть два инструмента:
* **namespaces** – (видимость) изолирует PID, Network, Mount (файлы и каталоги) и т. д.
* **Cgroups** – (ресурсы) изолирует CPU, RAM и т. д.

### отличия от VM

* VM использует гипервизор (ПО для запуска VM), который создает отдельные  виртуализированные ОС, выделяя им конкретную долю ресурсов.\
	обладает медленной загрузкой и ограниченными возможностями по миграции.
* Docker (система контейнеризации) использует ресурсы основной ОС (без процесса виртуализации).\

### архитектура

- Docker daemon – (фоновый процесс) сервис, который осуществляет всё взаимодействие с контейнерами.
- Docker client – интерфейс командной строки для управления Docker daemon.


## Основный понятия
 
 * **Docker image (образ)** – неизменяемый файл, из которого разворачиваются контейнеры. (состоит из слоев)
 
```sh
docker images  # показать локальные образы
docker {image} pull <img>:<tag>  # скачать образ из reqistry
docker {image} inspect <img>  # посмотреть слои образа и др. метаданные
docker {image} rm <img> # удалить образ # docker rmi <img>
```

* **Docker Registry** – хранилище с докер-образами. Чтобы каждый раз не собирать образ, его можно отправить в репозиторий, например Docker Hub. Платные - Docker Registry, Nexus, Harbor, Artifactory.

* **Dockerfile** – Текстовый файл с пошаговыми инмтрукциями для создания образа.

* **FROM** – базовый слой
* **RUN** – выполнить команду при сборке контейнера (создание нового слоя)
* **WORKDIR** – сменить базовую директорию
* **ENV** – пробросить переменную окружения
* **ARG** – параметры сборки
* **COPY** – копирование файлов
* **CMD** –  команда при старте контейнера

```Dockerfile
# ./Dockerfile
FROM python:3.11

RUN apt update && apt -y install gettext-base
WORKDIR /code
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

CMD ["python", "./main.py"]  # ./run.sh
```

```sh
# run.sh
python ./main.py
```

```Dockerfile
# ./Dockerfile
FROM ubuntu:20.04
RUN apt update && apt install -y nginx
CMD nginx -g 'deamon off;'
```

создать образ из Dockerfile:
```sh
docker {image} build -t <img> .
```

`.dockerignore` - перечисление файлов и каталогов, которые не будут включены в образ.


## Контейнеры

Запуск контейнера из образа:
```sh
docker {container} run --name=<conatiner> <img>  # --rm удалит контейнер при его остановке
docker run -p 80:80 docker/getting-started  # обучающий веб-сервис  # проброс портов (на мaшине : в контейнере)
docker run -p 80:80 -d nginx:1.20  # зауск в фоновом режиме конкретной версии nginx
```

**NGINX** – (др. Apache) веб сервис для раздачи статических файлов, который балансирует запросы между серверами.

 в этот момент:
1. инициализируется файловая система
2. выдается IP-адрес внутри сети docker
3. запускается команда `CMD` из Dockerfile и ей выдается PID 1

```sh
docker container ls  # посмотреть запущенные контейнеры
docker ps  # посмотреть запущенные контейнеры (устаревающая команда)
docker ps -a  # посмотреть и остановленные контейнеры

docker logs <container>  # посмотреть логи приложения
docker start <container>  # запустить остановленный контейнер
docker restart <container>  # перезапустить контейнер
docker pause <container>  # приостанавливает контейнер (с сохранением в памяти данных)
docker stop <container>  # остановить контейнер

docker rm <container>  # удалить контейнер
docker rm -f <container>  # удалить даже работающий контейнер
docker system prune  # удалить все остановленные контейнеры
```

```sh
docker exec <container> ls  # выпонить команду внутри контейнера
docker exec -it <container> /bin/bash  # в интерактивном режиме запустить консоль внутри контейнера

# внутри контейнера
apt update && apt install procps
ps aux  # посмотреть запущенные процессы (ps elf)
top  # тоже самое, но интерактивная
kill <PID>  # остановить процесс (1-ый останавливает контейнер)
exit  # выйти
```


## Сеть

**bridge** – виртуальная сеть внутри docker для обьщения между контейнерами.\
**host** – делить сетевое пространство с машиной.\
**none** – без сети.

Создание сети:
```sh
docker network ls  # посмотреть созданные сети
docker network create <net>  # создать сеть
docker network inspect <net>  # детальная информация

docker run --network=<net> <img>  # подключить контейнер к сети.
```

```Dockerfile
# ./Dockerfile
FROM ubuntu:20.04
RUN apt update && apt install -y nginx
CMD nginx -g "deamon off"
```

```sh
docker build -t <img> .
docker run -p 80:80 -d <img>
docker kill <container>  # останавливает контейнер (принудительное завершение)

curl localhost:80  # http запрос
curl -I localhost:80  # HEAD

# внутри контейнера
apt update && apt install net-tools
ifconfig  # показать текущие IP-адреса
```

### DNS в docker

```sh
docker network create <net>
docker run -p 80:80 -d --network=<net> --network-alias=<domain> <img>

# внутри контейнера
apt update && apt install dnsutils
host <domain>  # показать сопоставленный IP-адрес
```


## Запуск [PosgreSQL](https://www.postgresql.org/download/)

```sh
docker run -d
	--network <net>
	--network-alias <domain>
	-p 5432:5432
	-e POSTGRES_USER=<user>  # по умолчанию postgres
	-e POSTGRES_PASSWORD=<password>  # прокинуть переменные окружения
	-e POSTGRES_DB=<dbname>  # по умолчанию postgres
	--name <container>_pg
	postgres
```

```python
SQLALCHEMY_DATABASE_URL = 'postgresql://<user>:<password>@<domain>/<dbname>'
```

### Файловая система

Образ состоит из слоев. **Слой** – добавление файлов поверх предыдущего слоя, каждый слой имеет свой хэш. Первый слой - базовый, "scratch".

```Dockerfile
# ./Dockerfile
FROM python:3.10-slim

ENV HOME /code
WORKDIR HOME 
COPY requirements.txt .
RUN python -m pip install -r requirements.txt  # что редко изменяется, спрятано глубже
COPY app.py .
COPY migrations migrations
COPY docker_config.py default_config.py  # потом это делается через CI/CD 
 
CMD flask run -h 0.0.0.0 -p 80
```

Запуск двух контейнеров в одной сети (с postgres):
```sh
docker run --network <net> -p 80:80 --name <container> -d <img>
--platform=linux/amd64  # (у apple M1 arm)

# внутри контейнера
flask db upgrade  # применение миграций
```

```sh
docker exec flask-app ls  # посмотреть файлы в контейнере
docker exec -it flask-app /bin/bash  # подключиться внутрь к контейнеру
root $ > apt upgrate
root $ > apt install procps
root $ > ps aux
root $ > kill <PID>
root $ > flask db upgrade  :: применение миграций
```


***

## Docker volumes

При создании контейнера выделяется специальный слой, в котором хранятся все изменения файловой системы. Все слои хранятся в `/var/lib/overlay{2}/<id>`.

Посмотреть ID слоя:
```sh
docker {conteiner} inspect <conteiner> # посмотреть слои контейнера и др. метаданные
```

Stateless файлы хранятся в  `/var/lib/docker/overlay{2}/<id>`, и удаляются при завершении контейнера (эфимерность).

**Volume** – инструмент для хранения файлов в директории `/var/lib/docker/volumes` или в пробросанной папке с хоста, т. е. такой слой, который выделяется контейнеру, и не удаляется после его удаления.

Для поиска этой дирректории в Mac OS или Windows:
```sh
docker run -it --privileged --pid=host justincormack/nsenter1  # создание привилегированного контейнера
ls /var/lib/docker/overlay/  # внутри контейнера
```

В Volume можно хранить:
* данные DB
* файлы, добавляемые пользователем,
* файлы конфигурации (подменять стандартные)
* при разработке пробрасывать код внутрь контейнера

Основные команды:
```sh
docker volume ls  # посмотреть созданные volumes
docker volume create <volume>  # создать volume
docker volume inspect <volume>   # детальная информация
docker volume rm <volume>  # удалить
docker volume prune  # удалить все неиспользуемые в данный момент volumes

docker run -v <volume> :/dir_in_container <img>  # проброс volume в контейнер
docker run -v /dir_in_host:/dir_in_container <img>  # монтирование директории с хоста в контейнер

# пример для postgers
docker run ... -v $(pwd)/pg_data:/var/lib/postgresql/data postgres
```


## Docker Compose

 – инструмент для одновременного управления несколькими контейнерами, которые входят в состав одного приложения.
 
 В одном файле описывается весь состав приложения:
 * контейнеры
 * сети
 * volumes-тома
 * порядок запуска контейнеров
 
```yaml
# .\docker-compose.yaml
version: "3.9"
services:  # описание контейнеров
  api:  # название контейнера
    build:  # собрать образ перед запуском
      context: .
    ports:
    - 8000:80
  postgres:
    image: postgres:latest  # готовый образ
    environment:
      POSTGRES_PASSWORD: password
```
 
Основные команды:
```sh
docker-compose up -d # запустить всё приложение в режиме демона
docker-compose up --build  # запустить всё с пересборкой из Dockerfile
docker-compose start # запустить контейнеры
docker-compose stop  # остановить контейнер
docker-compose down  # остановить контейнеры и удалить все компоненты
docker-compose build  # cобрать образы  
docker-compose pull  # скачать необходимые образы
docker-compose logs  -f # посмотреть логи сервисов в режиме реального времени
docker-compose exec -it <service> /bin/bash  # войти внутрь контейнера
```

### порядок запуска Docker Compose

1) запустить PostgreSQL
2) применить миграции
3) запустить приложение

`depends_on` секция позволяет указать порядок запуска сервисов по условию:
- **service_started** – просто порядок запуска;
- **service_healthy** – запустить только после того, как контейнер будет работать (пройдет healthcheck);
- **service_completed_successfully** – запустить только после того, как успешно завершится другой контейнер.

```yaml
# .\docker-compose.yaml
version: "3.9"
services:
  api:
    build:
      context: .
    image: <login>/<repo>  # для команды pull
    ports:
      - 8000:80
    volumes:
      - ./docker_config.py:/code/default_config.py
    depends_on:  # порядок запуска
      postgres:
        condition: service_healthy
      migrations:
        condition: service_completed_successfully
  migrations:
    build:
      context: .
    image: <login>/<repo>
    volumes:
      - ./docker_config.py:/code/default_config.py
    depends_on:
      postgres:
        condition: service_healthy
    command: flask db upgrade  # переобределение CMD из Dockerfile
  postgres:
    image: postgres:latest
    environment:
      POSTGRES_USER: flask_app
      POSTGRES_PASSWORD: password
      POSTGRES_DB: flask_app
    volumes:
      - ./postgres-data:/var/lib/postgresql/data
    healthcheck:  # секция, которая определяет когда контейнер корректно запущен и готов к работе
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 5s
      retries: 5  # количество провальных попыток 
```
 
 
 ## Деплой через Docker Compose на сервер
 
1) собрать образы и отправить в registry:
```sh
docker login
docker-compose build
docker-comose push
# или, если нет секции image:
docker build -t <login>/<repo>:<tag> .
docker push <login>/<repo>:<tag>
```

2) установить [docker на VM](https://docs.docker.com/engine/install/ubuntu/):
```sh
# sudo apt -y install curl
sudo su
curl ...
echo ...
apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io
```

3) установить [docker-compose на VM](https://losst.pro/ustanovka-docker-compose-v-ubuntu-20-04):
```sh
curl ...
chmod ...
ls -s /usr/local/bin/docker-compose /usr/ bin/docker-compose
```

4) копируем yaml на сервер и запускаем:
```sh
scp docker_config.py <login>@<domain>:<project_name>/default_config.py
scp docker-compose.yaml <login>@<domain>:<project_name>
docker-compose up -d
```


### Docker Swarm

– позволяет обеспечивать взаимодействие между контейнерами в том случае, если контейнеры находятся на разных физических docker хостах.

Kubernetes и Swarm – это оркестраторы контейнеров, которые позволяют управлять большими кластерами Docker-хостов и координировать запуск и остановку контейнеров на них.
