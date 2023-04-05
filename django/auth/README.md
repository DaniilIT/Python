# Пользователи

в Django:
* **есть**:
    готовая модель, группы, система хэширования паролей, форма регистрации
* **нет**:
    проверки надежности пароля, защиты от DDoS-аттак, аутентификации через внешние системы

**батарейки** - фреймворки, написанные для расширения функционала django-приложений.

```shell
./manage.py startapp authentication
```

Расширить поля стандартной модели:
```python
# authentication/models.py
from django.contrib.auth.models import User, AbstractUser

# Profile(models.Model) - новая таблица c ForeignKey
# Profile(User) - новая таблица с id на User
class User(AbstractUser):  # swappable = "AUTH_USER_MODEL"
    MALE = 'm'
    FEMALE = 'f'
    SEX = [(MALE, 'Male'), (FEMALE, 'Female')]  # для отображения в django формах

    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    sex = models.CharField(max_length=1, choices=SEX, default=MALE)
```

Откатить миграции для встроенного auth, и накатить свежие:
```sh
./manage.py migrate auth zero
./manage.py makemigrations
./manage.py migrate
```

Переопределяем модель User для всего приложения
```python
# project_name/settings.py

AUTH_USER_MODEL = 'authentication.User'
```


## Регистрация

```python
# authentication.serializers.py

class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        # user = super().create(validated_data)
        user = User.objects.create(**validated_data)
        
        # user.set_password(user.password)
        user.set_password(validated_data['password'])  # хэширование
        user.save()
        
        return user
```

```python
# authentication/views.py
from rest_framework.generics import CreateAPIView
from authentication.models import User
from authentication.serializers import UserCreateSerializer

class UserCreateView(CreateAPIView):
    model = User
    serializer_class = UserCreateSerializer
```

```python
# authentication/urls.py
from django.urls import path
from authentication.views import UserCreateView

urlpatterns = [
    path('create/', UserCreateView.as_view()),
]
```
    

## Aутентификации

\- процедура проверки подлинности данных, например: аутентификация пользователя - это проверка введенного пароля на соответствие с паролем, сохраненным в DB.

**Авторизация** - предоставление *определенным* пользователям (или группе) прав на выполнение определенных действий.

### Авторизация по AuthToken

Подключить библиотеку и настроить проверку токенов:
```python
# project_name/settings.py

INSTALLED_APPS = [
    'rest_framework',
    'rest_framework.authtoken',
]

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': TOTAL_ON_PAGE,
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ]
}
```

у этой библиотеки есть свои миграции

```sh
./manage.py migrate
```

реализовать закрытие доступа:
```python
# authentication/views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

class LogOut(APIView):
    def post(self, request, format=None):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)
```

Настроить ручки:
```python
# authentication/urls.py
from django.urls import path
from rest_framework.authtoken import views
from authentication.views import LogOut

urlpatterns = [
    path('login/', views.obtain_auth_token),
    path('logout/', LogOut.as_view()),
]
```

для получения доступа к ресурсу в headers неоходимо добвить:
`Authorization: Token <your_token>`


### Авторизация по JWT

Токен не хранится на сервере.\
Реализуется через:
- access - краткосрочный токен
- refresh - долгосрочный токен
Разделен (через .) на три части:
* header - зашифрован используемый алгоритм
* payload - зашифрована информация, например id пользователя
* signature (подпись) - нужен для проверки на валидность


```sh
poetry add  djangorestframework-simplejwt
```

Добавить библиотеку в приложение и настроить его на проверку JWT:
```python
# project_name/settings.py

INSTALLED_APPS = [
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_simplejwt',
]

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': TOTAL_ON_PAGE,
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ]
}
```

Настроить ручки:
```python
# authentication/urls.py
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('token/', TokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
]
```

для получения доступа к ресурсу в headers неоходимо добвить:
`Authorization: Bearer <your_token>`


## Permission

\- Класс, который проверяет доступ пользователя к какой-либо функциональности.

```python
from rest_framework.permissions import IsAuthenticated

class VacancyDetailView(RetrieveAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancyDetailSerializer
    permission_classes = [IsAuthenticated]  # проверка доступа

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_vacancies(request):
    pass

class VacancyCreateView(CreateAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancyCreateSerializer
    permission_classes = [IsAuthenticated, VacancyCreatePermissions]  # добавление своей проверки
```

```python
# app_name/permissions.py
from django.contrib.auth.models import AnonymousUser
from rest_framework import permissions
from authentication.models import User

class VacancyCreatePermissions(permissions.BasePermission):
    message = "Adding vacancies for non hr user not allowed."  # текст ошибки
    
    def has_permission(self, request, view):
        if isinstance(request.user, AnonymousUser):
            return False
        return request.user.role == User.HR
```

### содздать суперпользователя

```sh
./manage.py createsuperuser
```
