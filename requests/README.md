# [Requests](https://requests.readthedocs.io/en/latest/)

\- библиотека для HTTP-запросов.

**HTTP** (HyperText Transfer Protocol) - протокол прикладного уровня для передачи данных по сети.\
**Протокол** - набор правил и соглашений, который определяет обмен данными между различными программами.

**MAC адрес** - уникальный физический адрес сетевого устройства (от производителя).

**IP** - уникальный адрес устройства в сети (от провайдера).

**OSI** - модель совместимости различных сетевых устройств, состоящий из уровней:

[7] *Приложений (application)* прикладной уровень, протоколы HTTP, FTP, SMTP, SSH(удаленное упр. ОС);\
[6] *Представления (presentation)*: кодирование данных;\
[5] *Сеансовый (session)*: синхронизация и определение прав доступа;\
[4] *Транспортный (transport)* (TCP, UDP): обеспечение целостности доставки;\
[3] *Сетевой (network)* (IP): маршрутизация, составление пакетов;\
[2] *Канальный (data link)* (MAC): составление фреймов;\
[1] *Физический (physical)*: передача двоичных данных;

**WAN** - Wide Area Network - Глобальная сеть, неограниченная географической локацией, в отличии от **LAN**.

**URL** - унифицированный указатель ресурсов, то есть ссылка на объект в Интернете.

* `https://` - схема, сетевой протокол;
* `www.` - субдомен;
* `example.com` - **доменное имя (domain)** - символьное представление IP;
* `:8080` - порт для определения типов данных (80-HTTP / 443-HTTPS);
* `/path/index.html` - адрес к файлу;
* `?id=1&n=10` - параметры;
* `#anchor` - якорь на html-странице;

С помощью запроса по **DNS** протоколу провайдер сообщает IP адрес.

**API** - интерфейс прикладного программирования, набор протоколов, которые определяют взаимодействие между приложениями. 

<img src="images/requests.webp" alt="Logo requests" title="logo requests" style="height: 380px;" />

Методы запросов:

* **GET** - извлечение данных из определенного ресурса;
* **HEAD** - запрос ресурса без тела ответа;
* **POST** - отправка сущностей и создание ресурса в теле запроса;
* **PUT** - изменение ресурса;
* **PATCH** - изменение части ресурса;
* **DELETE** - удаление ресурса;
* **OPTIONS** - определение параметров связанных с ресурсом;

**REST** стиль веб-архитектуры, который описывает принципы взаимодействия клиента и сервера.

```python
import requests


def make_request(token, param):
    url = f'{SITE_URL}/recurse/'
    headers = {'Authorization': token}
    payload = {'param': param, 'q': ''}
    response = requests.get(url, headers=headers, params=payload,
                            timeout=5, verify=False)  # проверка SSL
    # with open(filename, 'rb') as file:
    #     files = {'media': file}
    response = requests.post(url, data=payload, json=payload, files=files)
    # print(response.headers)
    
    # response.status_code  # 200
    # response.ok  # False если код >= 400
    # response.history  # [<Response [301]>]
    # response.is_redirect  # True
    response.raise_for_status()  # raise exception если код >= 400 (запрос завершился неудачно)

    # with open(filename, 'wb') as file:
    #     file.write(response.content)
    # text = response.text()
    data = response.json().get('key')
    return data


def main():
    requests.packages.urllib3.disable_warnings(
        requests.packages.urllib3.exceptions.InsecureRequestWarning
    ) # если (verify=False), то это отключает предупреждения
        
    try:
        data = make_request(token, param)
    except requests.exceptions.HTTPError as error:
        stderr.write('Вы ввели неправильную ссылку или неверный токен.')
        exit(f'Can\'t get data from server:\n{error}')
    except requests.exceptions.ConnectionError:  # при разрыве сессии
        logging.warning(f'Соединение с сервером на странице прервано.')
        sleep(5)
```

Код состояния HTTP:

1. **Informational**\
    *102 Processing (в обработке) - сервер получил запрос;
2. **Success**\
    *200 OK - сервер успешно обработал запрос;\
    *201 Created - сервер успешно создал ресурс (PUT);
3. **Redirection**\
    *301 Moved Permanently (перемещен на постоянной основе) - URI ресурса был изменен (напр: подставляет '/' в конец);
    *302 Found (найдено) - ресурс временно изменен (напр: пересылка на главную страницу);
4. **Client Error**\
    *401 Unauthorized - нет доступа без аутентификации;\
    *403 Forbidden - нет доступа с аутентификацией как у клиента;\
    *404 Not Found - сервер не может найти запрашиваемый ресурс;\
    *405 Method Not Allowed - сервер получил запрос с методом, который не ожидал (GET и HEAD разрешены всегда);
5. **Server Error**\
    *503 Service Unavailable - сервер временно перегружен или на тех. обслуживании;

---

URL - адрес, PATH в ОС - путь.

```python
from urllib.parse import urljoin, urlparse, unquote


url = 'https://www.example.com:8080/folder/index.html?id=1&n=10#anchor'

url_components = urlparse(url)
print(url_components)  # синтаксический анализ URL
# ParseResult(scheme='https', netloc='www.example.com:8080',
# path='/path/index.html', params='', query='id=1&n=10', fragment='anchor')

print(f'{url_components.netloc}{url_components.path}')  # 'www.example.com:8080/path/index.html'

url = urljoin('https://example.com/fol/', 'der/')  # если от корня, то '/der/'
print(url)  # https://example.com/fol/der/

print(unquote('/fol%20der/'))  # /fol der/


response = requests.get('https://www.google.ru/search', params={'q': 'гугл ить'})
print(response.url)  # https://www.google.ru/search?q=%D0%B3%D1%83%D0%B3%D0%BB+%D0%B8%D1%82%D1%8C
print(unquote(response.url))  # https://www.google.ru/search?q=гугл+ить
```

 ---

## [Beautiful Soup](https://beautiful-soup-4.readthedocs.io/en/latest/#css-selectors)

\— это библиотека Python для синтаксического анализа файлов HTML и XML.

**Парсер** — это программа, которая скачивает из интернета странички и разбирает их на составляющие.

```
pip install beautifulsoup4
pip install lxml
```

```python
from bs4 import BeautifulSoup

soup = BeautifulSoup(response.text, 'lxml')

cards = soup.find('main').find('table', class_='ct').find_all('div', class_='cd')
imgs = []
for card in cards:
    imgs.append(card.find(img))

# селекторы - правила для поиска элементов html.
title = soup.select_one('h1')
imgs = soup.select("main table.ct .cd img")
for img in imgs:
    img = unquote(img['src'])
```
