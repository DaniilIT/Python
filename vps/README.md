## Публикация приложений

* **Виртуальный хостинг**
	У всех проектов общие ресурсы: процессор и оперативная память.\
	Нет возможности настраивать операционную систему под себя. 

* **Выделенный сервер**
	Администраторский доступ ко всему железу.

* **Виртуальная машина (VPS)**
	На одном «железе» размещается сразу несколько виртуальных «компьютеров».
	Есть возможности настраивать операционную систему под себя. 


# VPS

**Гипервизор** - специальное ПО, который позволяет запускать изолированные виртуальные машины,\
то есть распределяет ресурсы между несколькими ОС.

* программная - VirtualBox, Parallels
* аппаратная - KVM, VMware, vSphere, Hyper-V

Подключение к виртуальной машине (серверу) и управление происходит с помощью сетегого протокола прикладного уровня SSH (Secure Shell) и программы  **OpenSSH Daemon (sshd)** - демон (работает в фоновом режиме).

Все данные, которые проходят по SSH-протоколу, шифруются  с помощью публичного и приватного (для расшифоровки) ключа.

создать SHH ключи:
```shell
ssh-keygen -t rsa
```

Публичный ключ надо положить на сервер в #.ssh/id_rsa.pub

[урок](https://skyengpublic.notion.site/25-1-8f89fad8c11e47db8e028c470ef90816)
[Yandex Cloud](https://cloud.yandex.ru/docs/managed-kubernetes/operations/node-connect-ssh)
[Благодаря DNS мы можем дать нашей виртуальной машине человекопонятный адрес.](https://www.freenom.com/ru/index.html?lang=ru)

Создание VM
1) https://cloud.yandex.ru/
2) подключиться
3) Computer Cloud
4) Создать BM
5) ...
6) Cloud DNS - привязать доменное имя (зона: `***.ga.`).


## подключение:

```shell
ssh login@xxx.xxx.xxx.xxx

ssh login@***.ga
```

посмотреть запущенные процессы:
```shell
ps aux
```

попсмотреть кто обслуживает доменное имя:
```shell
dig +trace ***.ga  :: например ns1.yandexcloud.net
```

DNS используется не только для получения адреса по доменному имени. типы DNS-записей:
* **А** - адрес веб-ресурса (IPv4-адрес), который соответствует введенному имени домена.
* **NS** - адрес DNS-сервера, отвечающего за содержание прочих ресурсных записей (делегирование).
* **MX** - адрес почтового сервера.
* **CNAME** - переадресация на другой домен.
* **TXT** - любая текстовая информация о домене.
* **SPF** - данные с указанием списка серверов, которым позволено отправлять письма от имени указанного домена.
* **SOA** - исходная запись зоны, в которой указаны сведения о сервере, содержащем образцовую информацию о доменном имени.

Посмотреть DNS-записи:
```shell
dig sky.pro any
``


## APT

Пакетный менеджер:
* устанавливает/обновляет/удаляет библиотеки и компоненты систем;
* устанавливает зависимости этих компонентов;
* следит за совместимостью пакетов друг с другом.

Пакет представляет собой набор файлов, необходимый для работы какого-либо ПО, и набор метаданных (версия пакета, его название и т. д.).

Ubuntu/debian: **apt**, MacOS: **brew**.

```shell
apt update  :: обновить БД пакетов
apt install python  :: установить пакет Python
apt remove python
apt install --reinstall python
``

Установка Python 3.10:
```shell
sudo su
add-apt-repository ppa:deadsnakes/ppa  :: обновление базы apt
apt install python3.10
``

Установка БД PostgreSQL:
```shell
apt install postgresql

sudo su postgres
createuser --interactive -P  :: flask_app_user, password, n, n, n
createdb flask_app --owner flask_app_user 
psql -U flask_app_user -h 127.0.0.1 flask_app
\l  :: посмотреть доступные DB
```

Установка venv:
```shell
apt install python3.10-venv

python3.10 -m venv env
. env/bin/activate
```


## Загрузка кода приложения на сервер

* копирование файлов через FTP
* копирование файлов через Git
* копирование файлов через SSH

**SCP** - утилита для копированя файлов поверх SSH.

```shell
scp test.txt malenko@51.250.22.196:test.txt  :: копирование одного файла
scp -r dir/ malenko@51.250.22.196:.  :: копирование директории

scp -r dir_name malenko@***.ga:flask_app    :: копирование директории
```


## systemd

\- система инициализации ОС (запускает процессы при старте системы)

юнит-файл:
```
# /etc/systemd/system/flask-api.service

[Unit]
Description=Flask-app
After=network.target

[Service]
WorkingDirectory=/opt/app/flask-app/
ExecStart=/opt/app/env/bin/python -m flask run -h 0.0.0.0 -p 80
Environment="APP_SETTINGS=/etc/flask-app/config.py"
Restart=always

[Install]
WantedBy=multi-user.target
```

чтобы systemd подтянул новую конфигурацию:
```shell
systemctl daemon-reload
```

«включаем» сервис:
```shell
systemctl start flask-api  :: название берется из названия unit-файла
```

посмотреть работу приложения:
```shell
systemctl status flask_app
```
