# FastAPI

<img src="images/logo.png" alt="logo FastAPI" title="Logo FastAPI" style="height: 240px;" />

Преимущества:
* асихронность
* прост в освоении
* отличная документация
* автоматическая документация (swagger)
* типизация (помогает валидировать запросы)

Недостатки:
* недостаточно большое community (по сравнению с django)

[Лучшие практики и пример](https://github.com/zhanymkanov/fastapi-best-practices)


## Установка

```shell
pip install fastapi[all]
```

К нему установятся:
* pydantic – библиотека для валидации и сериализации данных
* starlette – асихронный фреймворк (фунндамент для fastapi)
* uvicorn – при запуске веб-сервера обработывает запросы
* markupsafe
* python-dotenv
* websockets
* email-validator
* jinja2


## Quick Start

```python
# main.py
from fastapi import FastAPI
from starlette import status

app = FastAPI(
    title="My App"
)

# router = APIRouter(
#     prefix='/users',
#     tags=['users'],
#     responses={401: {'user': 'Not authenticated'}}
# )
app.include_router(user_router)

# post, put, patch, delete
@app.get('/', response_model=List[User],
         status_code=status.HTTP_200_OK)
async def hello():
    # raise HTTPException(
    #     status_code=404,
    #     detail='Item not found',
    #     headers={'X-Header-Error': 'Nothing to be seen at the UUID'}
    # )
    return {'message': 'Hello world!'}
```


### Запуск

```shell
uvicorn main:app --reload  # перезагружать сервер при изменении контекста
gunicorn main:app -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000 -w 2
```

Документация будет доступна сразу по адресу `/docs` и `/redoc`.


#### Передача URL Path параметров

```python
@app.get('/users/{user_id}')
def get_user(user_id: int, user_id: Annotated[int, Path(title="The ID of the user to get"), ge=1]):
	pass
```

Валидация типов происходит автоматически.
Annotated может быть использован для добавления метаданных.

#### Передача query параметров

```python
@app.get('/trades')
def get_trades(limit: int = 1, offset: int = 0,
               book_rating: int | None = Query(default=None, gt=0, lt=6),  # deprecated
               q: Annotated[str | None, Query(max_length=50)] = None):
    return fake_trades[offset:][:limit]
```

#### Передача тела запроса

```python
@app.post('/users/')
def create_item(item: Item,
                in_body: Annotated[int, Body(gt=0)):
    return {'status': 200, 'data': item}
```

параметр должен быть объявлен как тип модели Pydentic.

#### Передача формы

```python
@app.post('/login')
def bool_login(username: str = Form(), password: Annotated[str, Form()]):
    pass
```

#### Передача заголовок

```python
@app.post('/header')
def bool_login(header_1: Optional[str] = Header(None),
               user_agent: Annotated[str | None, Header()] = None):
    pass
```

Вернуть ответ напрямую

```python
@app.get("/portal")
async def get_portal(teleport: bool = False) -> Response:
    if teleport:
        return RedirectResponse(url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    return JSONResponse(content={"message": "Here's your interdimensional portal."})
```


## Depends

– отвечает за инъекцию зависимостей, функция, которая испольует результат внешней функции

```python
async def common_parameters(q: str | None = None, skip: int = 0):
    return {'q': q, 'skip': skip}

@app.get('/items/')
#async def read_items(commons: Annotated[dict, Depends(common_parameters)]):
async def read_items(commons: dict = Depends(common_parameters)):
    return commos
```

```python
async def verify_token(x_token: Annotated[str, Header()]):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")

async def verify_key(x_key: Annotated[str, Header()]):
    if x_key != "fake-super-secret-key":
        raise HTTPException(status_code=400, detail="X-Key header invalid")
    return x_key

@app.get("/items/", dependencies=[Depends(verify_token), Depends(verify_key)])
async def read_items():
    return [{"item": "Foo"}, {"item": "Bar"}]
```  

```python
# одно и то же
async def get_current_user(access_token: Annotated[str, Depends(oauth2_scheme)]):
async def get_current_user(access_token: str = Depends(auth2_scheme)):
```


## Pydantic

```python
from datetime import datetime
from enum import Enum
from uuid import UUID
from pydantic import BaseModel, Field

class Coordinate(BaseModel):
    lat: float
    lng: float

class DegreeType(str, Enum):
    newbie = 'newbie'
    expert = 'expert'

class Trade(BaseModel):
    id: UUID
    user_id: int = 1
    email: EmailStr
    currency: str = Field(max_length=5, title='...')
    price: float = Field(5, ge=0)
    select: DegreeType
    coordinates: Optional[Coordinate]
    created_at: datetime
    
    class Config:
        orm_mode = True
        schema_extra = {
            'example': {
                'id': '1fa85f64-5717-4562-b3fc-2c963f66afa6',
                'rating': 10
            }
        }
```

```python
@app.post('/trades', response_model=List[Trade])
def add_trades(trades: List[Trade]):
    # trades == [{"id": 0, "user_id": 0, "currency": "strin", "side": "string", "price": 0, "coordinates": {...}},]
    # new_book = Book(**book_request.dict())
    return {"status": 200, "data": trades}
```


## Exception

```python
# raise HTTPException(
#     status_code=HTTP_401_UNAUTHORIZED,
#     detail="Not authenticated",
#     headers={"WWW-Authenticate": "Bearer"},
# )

def raise_item_cannot be_found_exception():
	return HTTPException(status_code=404, detail='Item not found', headers={'x-Header_error': '...'})

raise raise_item_cannot be_found_exception()

class NegativeNumberException(Exception):
    def __init__(self, books_to_return):
    	self.books_to_return == books_to_return

raise NegativeNumberException(books_to_return)

@app.exception_handler(NegativeNumberException)
async def negative_number_exception_handler(request: Request,
exc: NegativeNumberException):
    return JSONResponse(
        status_code=status.HTTP_418...,
        content={'message': f'Hey, why do you want {exc.books_to_return} '
        f'books? You need to read more!'
    )

# Благодаря этой функции клиент видит ошибки, происходящие на сервере, вместо "Internal server error"
@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors()}),
    )

# Когда pydantic не сможет провалидировать при отправке с сервера:
{
  "detail": [
    {
      "loc": [
        "response",
        0,
        "name"
      ],
      "msg": "str type expected",
      "type": "type_error.str"
    }
  ]
}
```


## Alembic

```shell
pip install sqlalchemy alembic pcycorg2 asyncpg aiosqlite
```

```shell
alembic init migrations
# создастся `alembic.ini`
# sqlalchemi.url = postgresql+asyncpg://%(DB_USER)s:%(DB_PASS)s@%(DB_HOST)s:%(DB_PORT)s/%(DB_NAME)s?async_fallback=True  # DSN 
# DATABASE_URL = f'postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
# DATABASE_URL = 'sqlite+aiosqlite:///./add_db.db'
alembic revision --autogenerate -m "..."  # makemigrations
alembic upgrade head  # migrate
```

* query – (filter) используется в SQLAlchemy ORM, предоставляет объектно-ориентированный способ взаимодействия с базой данных через объекты модели.
* stmt – (where) используется в SQLAlchemy Core,  предоставляет прямой доступ к SQL-запросам, используется в асинхронном режиме.

### Read

```python
async with AsyncSession() as session:
    stmt = select(User).where(User.age > 18)
    result = await session.execute(stmt)
    users = result.all()
```

```python
stmt = select(User.name, Address).where(User.id == Address.user_id).order_by(Address.id)
```

```python
async with AsyncSession() as session:
    stmt = select(User).where(User.login == login)
    result = await session.execute(stmt)
    user = result.scalar()  # нет или много -> None
    user = result.scalar_one()  # нет или много -> Exception
    user = result.scalar_one_or_none()  # нет -> None # много -> Exception
```

```python
stmt = selectinload(User).where(User.login == login)  # подгрузить связанные объекты
```

```python
one_week_ago = datetime.now() - timedelta(weeks=1)
stmt = select(User).where(User..login == login).options(
    selectinload(User.posts).where(Post.date >= one_week_ago).selectone()
)
```

### Create

```python
stmt = insert(User).values(login=login, name=name)
await session.execute(stmt)
await session.commit()
```

```python
async def create_user(user_body: UserCreateSchema,
                      db: AsyncSession = Depends(get_db)):
    try:
        user_raw = user_body.dict(exclude_unset=True)
        new_user = User(**user_raw)
        db.add(new_user)
        await db.flush()
        await db.refresh(new_user)
        await db.commit()
    except IntegrityError:
        raise create_update_user_exception()
        
    return UserDetailSchema.from_orm(new_user)
```

### Update

```python
stmt = update(User).where(User.id == user_id).values(name=new_name)
await session.execute(stmt)
await session.commit()
```

### Delete

```python
stmt = delete(User).where(User.id == user_id)
await session.execute(stmt)
await session.commit()
```


## Аутентификация

(FastAPI-users)
(FastAPI-admin)

```shell
pip install 'fastapi-users[sqlalchemy]'
```


## database.py

```python
from typing import AsyncGenerator

from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

from config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER

DATABASE_URL = f'postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

Base = declarative_base()


engine = create_async_engine(DATABASE_URL, poolclass=NullPool) # движок не использует какое-либо соединение более одного раза
# connect_args={'check_same_tread': False}  # sqllite

async_session = async_sessionmaker(bind=engine, autoflush=False, autocommit=False,
                                   expire_on_commit=False)


# Dependency
# def get_db():
#     db = SessionLocal()  # async_session
#     try:
#         yield db
#     finally:
#         db.close()

# Dependency
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as db:
        yield db
```


## Redis

```shell
fastapi-cache2[redis]
```

```python
@app.on_event("startup")
async def startup_event():
    redis = aioredis.from_url("redis://localhost", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
```

```python
@router.get("/long_operation")
@cache(expire=30)
def get_long_op():
    time.sleep(2)
    return "Ready"
```
