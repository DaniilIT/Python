# Документация

**OpenAPI** - машиночитаемая схема (yaml, json), которая описывает всё, что есть в API: какие ресурсы доступны, какие у них URL, в каком формате они отображаются и какие операции поддерживают.

Виды интерактивной документации:
* Swagger
* ReDoc


### docstring

```sh
poetry add django-rest-swagger
```

```python
# ./project_name/urls.py
schema_view = get_schema_view(title='User API', renderer_classes=[OpenApiRenderer, SwaggerUIRenderer])
urlpatterns = [
    url(r'^', schema_view, name='docs'),
    url(r'^users/', include(router.urls)),
]
```

```python
class UserViewSet(viewsets.ModelViewSet):
    """
    retrieve:
        Return a user instance.
    
    list:
        Return all users, ordered by most recently joines.
    
    create:
        Create a new user.
    
    delete:
        Remove an existing user.
    
    partial_update:
        Update one or more fields on a existing user.
    
    update:
        Update a user.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
```

Батарейки для генерации документации:
* *drf-yasg* - OpenAPI2.0
* *drf-spectacular* - OpenAPI3.0


## drf-spectacular

Установка
```sh
poetry add drf-spectacular
```

```python
# ./project_name/settings.py

INSTALLED_APPS = [
    ...
    'drf_spectacular',
]

REST_FRAMEWORK = {
    ...
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'My  API',
    'DESCRIPTION': 'Awesome my project',
    'VERSION': '1.0.0',
}
```

```python
# ./project_name/urls.py
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
    ...
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),  # YAML
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema')),
]
```

## Кастомизация

```python
class ItenListView(ListAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    @extend_schema(
        request=MyRequestSerializer,
        responses=MyResponsesSerializer,
        description='Retrieve item list',  # 'Returns a single item'
        summary="Item list",  # 'Find item by ID'  # короткое описание
        deprecated=True  # устаревший метод (будет зачеркнутым)
    )
    def get(self, request, *args, **kwargs):
        pass

class ItemUpdateView(UpdateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    http_method_names = ['put']  # убрать patch из документации
```

```python
@extend_schema_view(
    list=extend_schema(description="Retrieve skills", summary="Skills list"),
    creatr=extend_schema(description="Create new skill object", summary="Create skill")
)
class SkillViewSet(ModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
```
