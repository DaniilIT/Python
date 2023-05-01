# python -m pip install 'fastapi[all]'
# uvicorn 15_0_server:app --reload
import asyncio
from fastapi import FastAPI

app = FastAPI()
lock = asyncio.Lock()
count = 0

@app.get('/')
async def main():
    global count

    # await lock.acquire()  # нацепить замок
    # count += 1
    # await lock.release()  # снять замок
    async with lock:
        count += 1

    return {'count': count}


@app.get('/hello')
async def greet():
    return {'msg': 'Hello world'}
