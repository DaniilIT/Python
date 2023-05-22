# [Django](https://www.djangoproject.com/)

– Веб-фреймворк для создания сайтов.\
В отличии от микрофреймворка Flask, Django нуждается в меньшем количестве ручной настройки приложения и не нуждается в дополнительных пакетах для работы с ORM.

<img src="images/django.jpeg" alt="logo django" title="Logo django" style="height: 240px;" />

Django построен по принципу **MVC**, но именуется **MTV**:
* Model – отображение данных в ООП формат $\rightarrow$ **Model**
* View – визуальная составляющая $\rightarrow$ **Template**
* Controller – бизнес-логика приложения $\rightarrow$ **View**

Приложение разделено на app-ы, python-пакеты, оформленные специальным образом, являющиеся небольшими отдельными web-приложениями.\
Файл `manage.py` - консольная утилита, с помощью которой создаются папки и файлы, генерируется шаблонный код, накатываются миграции и запускается приложение.


### poetry

– своременный пакетный менеджер, не такой "примитивный" как pip, например, позволяет управлять уровнями зависимостей.

```sh
pip install poetry  # установить
poetry init  # создание pyproject.toml
poetry add django  # pip install django
poetry add django@^3  # ==3.*
poetry install  # установить все зависимости
```


### Виртуальное окружение `virtualenvwrapper`

– это надстройка над `virtualenv` (инструмент для создания изолированных виртуальных окружений Python, которые позволяют изолировать зависимости проекта), которая предоставляет дополнительные функции, такие как автоматическое переключение между виртуальными окружениями.

```sh
python -m pip install virtualenvwrapper

python -V  # узанть версию
which python  # узнать расположение интерпертатора
export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
export VIRTUALENVWRAPPER_VIRTUALENV=/usr/local/bin/virtualenv
source /usr/local/bin/virtualenvwrapper.sh  # добавить нижеуказанные команды
```

```sh
mkvirtualenv myenv  # python -m venv myenv
workon myenv  # source myenv/bin/activate
deactivate

lsvirtualenv  # показать доступные окружения
cpvirtualenv myenv myenv_copy
rmvirtualenv myenv

mkproject myproject   # создать вместе с проектом
cdproject  # перейти в папку с проектом и активировать окружение
```


## Создать Django-приложение

```sh
django-admin startproject <project> .
./manage.py startapp <app>  # создать отдельный функционал
./manage.py runserver  # запустить сервер
```

подключение модуля приложения:
```python
# <project>/settings.py

INSTALLED_APPS = [
    ...
    '<app>',
]

MEDIA_URL = '/media/'  # адрес, по которому будут доступны файлы
MEDIA_ROOT = BASE_DIR.joinpath('media')  # путь, по которму хранятся файлы
```

Настройка интепретатора:
<img src="images/pycharm.png" alt="pycharm" title="pycharm" style="height: 320px;" />


## Создать модель

Модель – это класс, который описывает поля (столбцы) таблицы DB.\
Пример использование models.QuerySet as manager в [sensive-blog](https://github.com/DaniilIT/sensive-blog)

```python
# <app>/models.py
from django.contrib.auth.models import User
from django.db import models

class M(models.Model):
    # STATUS = [
    #     ('draft', 'Черновик'),
    #     ('open', 'Открыта'),
    #     ('closed', 'Закрыта')
    # ]
    class Status(models.TextChoices):
        DRAFT = 'draft', 'Черновик'
        OPEN = 'open', 'Открыта'
        CLOSED = 'closed', 'Закрыта'
    
    # id = models.BigAutoField(primary_key=True)
    slug = models.SlugField(max_length=50, unique=True)
    description = models.TextField('описание', null=True, blank=True)
    # status = models.CharField(max_length=6, choices=STATUS, default='draft')
    status = models.CharField(max_length=6, choices=Status.choices, default=Status.DRAFT)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='logos/')  # прибавляется к MEDIA_ROOT
    time_create = models.DateTimeField(default=timezone.now)
    created = models.DateField(auto_now_add=True)  # default=datatime.date.now
    is_activated = models.BooleanField(default=False)
    
    # связь O2M (User - One)  # on_delete - что делать при удалении записи, на которую ссылается FK
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,  # CASCADE  # создаст user_id
        verbose_name='Автор',
        limit_choices_to={'is_staff': True},
        null=True,
        blank=True
    )
    # связь M2M
    skills = models.ManyToManyField(
        Skill,
        related_name='return_to_m',
        verbose_name='Навыки'
    )
    
    # определение информации о модели для панели админки
    class Meta:
        verbose_name = 'Навык'  # название модели
        verbose_plural = 'Навыки'
        ordering = ['-name']  # сортировка, но выполняется ко всем запросам
    
    def __str__(self):
        return self.slug
```

null=True – заменять пустые значения на NULL в DB\
blank=True – разпешить пустые значения в админке, по-умолчанию обязателен\

<img src="images/fields.png" alt="fields" title="Fields" style="height: 580px;" />


### **Миграции** 

– фиксируют текущее состояние DB и помогают быстро развернуть DB с нуля.

```sh
./manage.py makemigrations
./manage.py migrate  # накатить
./manage.py migrate <app> migration_num | zero  # откатить
# после отката необходимо удалить файлы из migrations/

./manage.py loaddata ./data/file.json  # загрузить данные
```


## Создать URL

соеденить адреса с views

```python
# project/urls.py
from django.contrib import admin
from django.urls import path, include
from app_name import views
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('items/', views.index),
    path('', views.index),
    path('items/', views.ItemView.as_view()),  # expect callable
    path('items/<int:item_id>', views.get),
    path('user/<int:pk>/', views.UserDetailView.as_view()),  # pk or slug
    path('<app>/', include('<app>.urls'))  # подключить список
]

if settings.DEBUG:  # доступ к файлам
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

Допустимые параметры:
- `str` – любая непустая строка.
- `int` – 0 или любое положительное число.
- `slug` – строка из ASCII букв или чисел, а также дефисы и подчеркивание.
- `uuid` – универсальный уникальный идентификатор.
- `path` – непустая строка, включая /.


## Создать view

```python
# app_name/views.py
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from app_name.models import M

def hello(request):
    return HttpResponse('Hello world')
```


### вытащить URL-параметры

```python
def get(request, item_id):
    if request.method == 'GET':
        try:
            item = M.objects.get(pk=item_id)
        except M.DoesNotExist as exc:
            return JsonResponse({'error': str(exc)}, status=404)
        
        return JsonResponse({'id': item_id, 'field': item.field},
                                            json_dumps_params={"ensure_ascii": False})  # Кодировка
```


## GET запрос

```python
def index(request):
    if request.method == 'GET':
        items = M.objects.all()

        if search_field := request.GET.get('field'):  # принимает query-параметр
            items = items.filter(field=search_field)

        response = []
        for item in items:
            response.append({
                'id': item.id,
                'field': item.field,
            })

        return JsonResponse(response, safe=False,  # Передаем не словарь
                            json_dumps_params={"ensure_ascii": False})
```


## POST запрос

### CSRF

– вектор атаки, межсайтовой подделки запросов, при котором вредоностный сайт делает запрос как-будто он уже авторизован.

В django отключить проверку csrf-токена можно через декторатор:
```python
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def index(request):
    if request.method == "POST":
        item_data = json.loads(request.body)

        # item = M()
        # item.text = item_data.get('text')
        # item.save()
        item = M.object.create(field=item_data.get('field'), ...)
        
        return JsonResponse({'id': item_id, 'field': item.field}) 
```


## class-based view

– подход к написанию вьюшек через классы.

```python
import json
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import ValidationError
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from app_name.models import M, Skill

# @method_decorator(csrf_exempt, name='dispatch')
# class MView(View):
#    def get(self, request):
#        pass
#    
#    def post(self, request):
#        pass

class MListView(ListView):
    model = M
    
    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        # self.object_list == M.objects.all()
        
        if search_text := request.GET.get("text"):
            self.object_list = self.object_list.filter(text=search_text)
        
        response = []
        for item in self.object_list:
            response.append({...})
        
        return JsonResponse(response, safe=False)


class MDetailView(DetailView):
    model = M
    
    def get(self, request, *args, **kwargs):
        item = self.get_object()
        
        return JsonResponse({...})


@method_decorator(csrf_exempt, name='dispatch')
class MCreateView(CreateView):
    model = M
    fields = ('field', ...)  # список fields для автоматической генерации форм в django
    
    def post(self, request, *args, **kwargs):
        item_data = json.loads(request.body)
        
        user = get_object_or_404(User, pk=item_data['user_id'])
         
        item = M.objects.create(
            text=item_data['text'],
            ...
            user=user
        )
        
        for skill in item_data['skills']:
            skill_obj, created = Skill.objects.get_or_create(name=skill, defaults={
                'is_active': True
            })
            item.skills.add(skill_obj)
        
        return JsonResponse({...}, status=302)


@method_decorator(csrf_exempt, name='dispatch')
class MUpdateView(UpdateView):
    model = M
    fields = ('text', ...)
    
    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        
        item_data = json.loads(request.body)
        self.object.field = item_data['field']
        ...
        
        # для связи M2M
        for skill in self.object.skills.all():
            self.object.skills.remove(skill)
        for skill in item_data['skills']:
            # try:
            #     skill_obj = Skill.objects.get(name=skill)
            # except Skill.DoesNotExist:
            #     return JsonResponse({'error': 'Skill not found'}, status=404)
            skill_obj, is_created = Skill.objects.get_or_create(name=skill)  # get_object_or_404
            self.object.skills.add(skill_obj)
        
        try:
            self.object.full_clean()  # проверить ограничения полей
        except ValidationError as error:
            return JsonResponse(error.message_dict, status=422)  # Unprocessable Entity
        
        self.object.save()
        return JsonResponse({
            'text': self.object.text,
            'user': self.object.user_id,
            'skills': list(self.object.skills.all().values_list('name', flat=True)),
        })


# обновить картинку
@method_decorator(csrf_exempt, name='dispatch')
class NUpdateView(UpdateView):
    model = N
    fields = ['name', 'logo']
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        
        self.object.logo = request.FILES.get('logo')  # из формы
        self.object.save()
        
        return JsonResponse({
            'id': self.object.id,
            'name': self.object.name,
            'logo': self.object.logo.url if self.object.logo else None
        }, json_dumps_params={"ensure_ascii": False})


@method_decorator(csrf_exempt, name='dispatch')
class MDeleteView(DeleteView):
    model = M
    success_url = '/'  # перенаправить после удаления
    
    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)
        return JsonResponse({}, status=204)
        # return redirect(self.get_success_url())
```


## Панель Админки

– UI над DB и позволяет гибко настраивать доступ

```python
# app/admin.py
from django.contrib import admin
from items.models import M

# admin.site.register(M)

class TagPostInline(admin.TabularInline):
    model = Tag.posts.through
    raw_id_fields = ('tag',)

@admin.register(M)
class MAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'role')
    search_fields = ('username',)
    
    fields = (...)
    exclude = ('field',)
    list_filter = ('role',)
    readonly_fields = ('published_at',)
    raw_id_fields = ('likes',)
    
    inlines = [
        TagPostInline,
    ]
    
    def preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" style="max-height: 200px;">')
        return 'Файл не выбран'
```


### создать супер пользователя

```sh
./manage.py createsuperuser
```


## Postgres

подключение:
```python
# project_name/settings.py

DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': BASE_DIR / 'db.sqlite3',
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```


## Действия с DB

сортировка:
```python
self.object_list = self.object_list.order_by('name', '-last_name')
```

количество записей:
```python
total = self.object_list.count()
```

limit, ofset:
```python
# self.object_list == self.object_list[:total]
self.object_list = self.object_list[2:2+3]  # пропустить первые два и вывести три
```

#### Пагинация:

```python
paginator = Paginator(self.object_list, settings.TOTAL_ON_PAGE)
page_number = request.GET.get('page')
page_obj = paginator.get_page(page_number)
response = {
    'items': page_obj,
    'per_page': settings.TOTAL_ON_PAGE,
    'num_pages': paginator.num_pages,
    'total': paginator.count  # количество записей
}
```

### Группировка

#### Annotate:

добавляет колонку, в которой для каждой записи просчитывается результат

```python
from django.db.models import Count, Avg, Max

# users_qs = User.objects.annotate(total_items=Count('item'))
self.object_list = self.object_list.annotate(total_items=Count('item'))
```

query set – это запрос, произойдет который только при попытке вытащить данные

#### Aggregate:

посчитает общее значение по всей таблице

```python
avg_items = user_qs.aggregate(Avg('items'))  # {'items__avg': result}
avg_items = user_qs.aggregate(fuck=Avg('items'))['fuck']  # result

max_price = Book.objects.all().aggregate(Max('price'))  # {'price__max': result}
```

### Join

`select_related` – обратиться к колонке связной таблицы (нужна, т. к. по умолчанию django JOIN не делает)\
`prefetch_related` – для M2M заранее запрашивает данные из связной таблицы

```python
self.object_list = self.object_list.select_related('user')  # Left Join работает для Foreing Key
self.object_list = self.object_list.prefetch_related('skills')
```

```python
class MListView(ListView):
    model = M
    
    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        
        if search_text := request.GET.get("text"):
            self.object_list = self.object_list.filter(text=search_text)
        
        self.object_list = self.object_list.select_related('user').prefetch_related('skills').order_by('text')
        
        response = []
        for item in self.object_list:
            response.append({
                ...
                'id': item.id,
                'text': item.text,
                # 'user': item.user_id,  # колонка родной таблицы
                'user': item.user.username,  # если без select_related('user'), будет отдельный запрос для каждой записи
                # 'skills': list(vacancy.skills.all().values_list('name', flat=True)),  # будет отдельный запрос для каждой записи
                'skills': list(map(str, vacancy.skills.all()))  # если без prefetch_related('skills'), будет отдельный запрос для каждой записи
            })
        
        return JsonResponse(response, safe=False)
```
