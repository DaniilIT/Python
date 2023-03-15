# Docker

\- это платформа для разработки и запуска контейнеров, которая позволяет запускать несколько изолированнх приложений внутри одной виртуальной машины.

<img src="images/docker.webp" alt="docker" title="docker" style="height: 380px;"/>


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

COPY main.py /
CMD ["python", "./main.py"]
```

создать образ из Dockerfile:
```bash
docker build -t my_image .
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
FROM python:3.10

WORKDIR /code
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app.py .
COPY migrations migrations
COPY docker_config.py default_config.py

CMD flask run -h 0.0.0.0 -p 80
```

### Запуск PosgreSQL

Запуск двух контейнеров в одной сети:
```bash
docker run --name postgres  :: название контейнера
	-e POSTGRES_USER=flask_app  # прокинуть переменные окружения внутрь
	-e POSTGRES_PASSWORD=password
	-e POSTGRES_DB=flask-app
	--network flask_app
	--network-alias pg
	-d postgres  :: запустить в фоновом режиме

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
