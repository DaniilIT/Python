# Куча

Кодирование:
```
poetry add ansible-vault-win --dev 
ansible-vault encrypt deploy/.env --output deploy/vault.env
ansible-vault decrypt deploy/vault.env
```

Удалить файл из истории git:
```sh
git filter-branch -f --index-filter 'git rm --cached --ignore-unmatch ./src/.env'
git filter-repo --path ./src/.env --invert-paths  # современный способ
```

Запус pre-commit:
```
poetry add pre-commit --dev
pre-commit install
pre-commit sample-config > .pre-commit-config.yaml
pre-commit run -a 
```

Сгенерировать пароль:
```sh
openssl rand -hex 16
```

Подставить переменные из .env:
```sh
docker-compose config
```

Сгенерировать статику в django:
```sh
./manage.py collectstatic -c --no-input
```

снести docker-compose:
```sh
docker-compose down --rmi local -v
```

Подключиться к postgres
```sh
psql -U postgres -d postgres -h 127.0.0.1
```

OpenID предназначен для аутентификации — то есть для того, чтобы понять, что этот конкретный пользователь является тем, кем представляется. 
OAuth, — это возможность авторизоваться на удаленном сервисе (Service Provider) и делать автризованные запросы к API.
OAuth 2.0 — протокол авторизации, позволяющий выдать одному сервису (приложению) права на доступ к ресурсам пользователя на другом сервисе. 

queriset =  queryset используется в классах представлений, чтобы определить набор моделей, на которых будут выполняться операции чтения (Retrieve), обновления (Update) и удаления (Destroy).

SOAP (S imple O bject A ccess P rotocol, или простой протокол доступа к объектам) — это протокол, по которому веб-приложения взаимодействуют между собой или с клиентом.
REST API обычно считается более простым и быстрым для разработки и интеграции, в то время как SOAP API может быть полезным в случаях, требующих большей надежности и формализации.
Оба API могут использоваться для создания веб-служб, обеспечивающих взаимодействие между клиентами и серверами

CSRF (Cross-Site Request Forgery)
В атаке CSRF злоумышленник обманом заставляет невиновного конечного пользователя отправить веб-запрос, который он не намеревался.
