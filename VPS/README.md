## Публикация приложений

* **Виртуальный хостинг**
	У всех проектов общие ресурсы: процессор и оперативная память.\
	Нет возможности настраивать операционную систему под себя. 

* **Выделенный сервер (VDS)**
	Virtual Dedicated Server. Администраторский доступ ко всему железу.

* **Виртуальная машина (VPS)**
	Virtual Private Server. На одном «железе» размещается сразу несколько виртуальных «компьютеров».
	Есть возможности настраивать операционную систему под себя. 


# VPS

**Гипервизор** – специальное ПО, который создает и запускает изолированные виртуальные машины,\
то есть распределяет ресурсы между несколькими ОС.

* программная – VirtualBox, Parallels
* аппаратная – KVM, VMware, vSphere, Hyper-V

**Виртуальная машина** – среда, которая эмулирует ПО, используя ресурсы физического хоста.

Подключение к виртуальной машине (удаленному серверу) и управление происходит с помощью сетегого протокола прикладного уровня **SSH (Secure Shell)** и программы  **OpenSSH Daemon (sshd)** – демон (работает в фоновом режиме).

Все данные, которые проходят по SSH-протоколу, шифруются  с помощью публичного (для шифрования) и приватного (для расшифоровки) ключей.

создать SHH ключи:
```shell
ssh-keygen -t rsa  # -t ed25519  # алгоритм
cat .ssh/id_rsa.pub
# на сервере хранится в /home/<login>/.ssh/authorized_keys
```

Благодаря DNS (Domain Name System) мы можем дать виртуальной машине человекопонятный адрес.


## подключение:

```shell
ssh <login>@IP4
ssh <login>@<домен>  # ssh dmanuilov@daniilit.online
# войдет как <login>@<name>
sudo su  # root@<name> # режим администратора

logout  # exit  # выйти из VM
```

создать нового пользователя:
```shell
sudo su
adduser <user>  # задать пароль
usermod -aG sudo <user>  # дать права администратора
id <user>  # посмотреть в каких группах состоит
# vim /etc/ssh/sshd_config
# PasswordAuthentication no -> PasswordAuthentication yes
systemctl reload sshd  # service ssh restart

ssh -i ~/.ssh/<ssh> <login>@IP4  # войти с указанием ключа
sudo su - <user>  # поменять пользователя
```

```shell
# посмотреть запущенные процессы
ps aux

# посмотреть версию ОС
lsb_release -a
```

попсмотреть кто обслуживает доменное имя:
```shell
dig +trace <домен>  # например ns1.yandexcloud.net
dig <домен> any  # посмотреть записи
```

DNS используется не только для получения IP адреса по доменному имени. типы DNS-записей:
* **А** – адрес веб-ресурса (IPv4-адрес), который соответствует введенному имени домена.
* **AAAA** - для IPv6.
* **NS** – адрес DNS-сервера, отвечающего за содержание прочих ресурсных записей (кому делегирован).
* **MX** – адрес почтового сервера.
* **CNAME** – переадресация на другой домен, например прикрепление поддомена (www.site.ru -> site.ru).
* **TXT** – любая текстовая информация о домене.
* **SPF** – данные с указанием списка серверов, которым позволено отправлять письма от имени указанного домена.
* **SOA** – исходная запись настройки зоны, в которой указаны сведения о сервере, содержащем образцовую информацию о доменном имени.


## APT

– (Advanced Packaging Tool) пакетный менеджер:
* устанавливает/обновляет/удаляет библиотеки и компоненты системы;
* устанавливает зависимости этих компонентов;
* следит за совместимостью пакетов друг с другом.

Пакет представляет собой набор файлов, необходимый для работы какого-либо ПО, и набор метаданных (версия пакета, его название и т. д.).

Ubuntu/debian: **apt**, MacOS: **brew**.

Установка python:
```shell
sudo su
apt update && apt upgrade  # обновить БД пакетов
add-apt-repository ppa:deadsnakes/ppa  # установит репозиторий, чтобы можно было установить актуальный python
apt install python3.11  # установить python
apt-get install python-is-python3  # настроить ссылку

apt install --reinstall python  # обновить
apt remove python  # purge - полностью удалить
```

```shell
apt install git
apt install python3-pip
apt install python3-venv
apt install python3.11-venv

python3.11 -m venv venv
. venv/bin/activate  # source venv/bin/activate
```

Установка PostgreSQL:
```shell
apt install postgresql

sudo su postgres
createuser --interactive -P  # username, password, n, n, n  # права
createdb username --owner db_name 
psql -U username -h 127.0.0.1 db_name
psql -U username -d db_name -h 127.0.0.1
\l  # посмотреть доступные DB
\d  # посмотреть доступные таблицы
\q  # выход
```


## Перемещение файлов на сервер

* копирование файлов через FTP
* копирование файлов через Git
* копирование файлов через SSH

**SCP** – утилита для копированя файлов поверх SSH.

```shell
scp test.txt <login>@<name>:test.txt  # копирование файла
scp -r dir/ <login>@<name>:.  # копирование директории
```


## systemd

– система инициализации ОС (запускает процессы при старте системы)

юнит-файл:
```
# vim /etc/systemd/system/flask-api.service

[Unit]
Description=flask-app
After=network.target  # запуск после инициализации сети

[Service]
WorkingDirectory= /home/<login>/flask-app/  # /opt/app/flask-app/
ExecStart=/home/<login>/sky_flask/venv/bin/python -m flask run -h 0.0.0.0 -p 80
# ExecStart=/home/<login>/sky_flask/venv/bin/gunicorn app:app -b 0.0.0.0:80 -w 4
Environment="APP_SETTINGS=/home/<login>/config.py"
Envirenment="FLASK_APP=main.py"
Restart=always

[Install]
WantedBy=multi-user.target  # уровень запуска сервиса
```

подтянуть новую конфигурацию:
```shell
systemctl daemon-reload
```

включить сервис:
```shell
systemctl start flask-api  # название unit-файла
systemctl stop flask-api
systemctl enable flask-api  # включить восле перезагрузки
systemctl disable flask-api
```
 
посмотреть работу приложения:
```shell
systemctl status flask-api
```

посмотреть журнал вызовов:
```shell
journalctl -u flask-api -f -n 1000

# освободить порт
kill -9 $(lsof -t -i:80)
```
