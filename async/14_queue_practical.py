"""
The https://xkcd.com asynchronous crawler
"""

import asyncio
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
from urllib.parse import urlparse

import aiohttp
import aiofiles
from bs4 import BeautifulSoup

URL = 'https://c.xkcd.com/random/comic/'

async def make_request(url, session: aiohttp.ClientSession):
    response = await session.get(url)
    if response.ok:
        return response
    else:
        print(f'{url}, returned: {response.status}')


async def get_image_page(queue: asyncio.Queue, session):
    url = URL
    response = await make_request(url, session)
    await queue.put(response.url)


def _parse_link(html):
    soup = BeautifulSoup(html, 'lxml')
    image_link = 'https:' + soup.select_one('div#comic>img').get('src')
    return image_link


async def get_image_url(pages_queue: asyncio.Queue, image_urls_queue: asyncio.Queue, session):
    while True:
        url = await pages_queue.get()
        response = await make_request(url, session)
        html = await response.text()

        # запустить сихронный код парсера
        loop = asyncio.get_running_loop()
        with ProcessPoolExecutor() as pool:
            image_link = await loop.run_in_executor(
                pool, _parse_link, html
            )

        await image_urls_queue.put(image_link)

        pages_queue.task_done()


async def download_image(queue: asyncio.Queue, session):
    while True:
        url = await queue.get()
        response = await make_request(url, session)
        filename = Path(urlparse(url).path).name
        folder = Path('./pictures')
        folder.mkdir(exist_ok=True)

        async with aiofiles.open(folder.joinpath(filename), 'wb') as file:
            async for chunk in response.content.iter_chunked(1024):
                await file.write(chunk)

        queue.task_done()


async def main():
    session = aiohttp.ClientSession()
    pages_queue = asyncio.Queue()
    image_urls_queue = asyncio.Queue()

    page_getters = [asyncio.create_task(
        get_image_page(pages_queue, session)
    ) for i in range(5)]

    url_getters = [asyncio.create_task(
        get_image_url(pages_queue, image_urls_queue, session)
    ) for i in range(5)]

    downloaders = [asyncio.create_task(
        download_image(image_urls_queue, session)
    ) for i in range(5)]

    await asyncio.gather(*page_getters)

    await pages_queue.join()
    for task in url_getters:
        task.cancel()

    await image_urls_queue.join()
    for task in downloaders:
        task.cancel()

    await session.close()

if __name__ == '__main__':
    asyncio.run(main())
