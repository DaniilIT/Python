import asyncio


async def coro_norm():
    await asyncio.sleep(0)  # для маленьких задач
    return 'norm task done!'


async def coro_error():
    raise ValueError


async def coro_long():
    try:
        print('Long task is running...')
        await asyncio.sleep(2)
        print('Long task completed')
    except asyncio.CancelledError:
        print('Long task cancelled')
        raise asyncio.CancelledError  # чтобы задача получила статус отмененной
    else:
        return 'long task done!'


async def main():
    # task1 = asyncio.create_task(coro_norm())
    # task2 = asyncio.create_task(coro_error())
    # task3 = asyncio.create_task(coro_long(), name='long_task')
    # tasks = [task1, task2, task3]
    # try:
    #     results = await asyncio.gather(*tasks)
    try:
        async with asyncio.TaskGroup() as tg:
            task1 = tg.create_task(coro_norm())
            task2 = tg.create_task(coro_error())
            task3 = tg.create_task(coro_long(), name='long_task')
        results = [task1.result(), task2.result(), task3.result()]

    # except ValueError as e:
    except* ValueError as e:
        # в TaskGroup отмена всех задач происходит автоматически
        print(f'{e=}')
    else:
        print(f'{results=}')

    # в gather отмена задач происходит вручную
    # for task in tasks:
    #     if task.done() is False:
    #         task.cancel()
    # ожидаем пока все задачи завершают отмену
    # await asyncio.sleep(1)
    # for task in tasks:
    #     print(f'task {task.get_name()} is {task._state}')  # 'FINISHED' or 'CANCELLED'


if __name__ == '__main__':
    asyncio.run(main())
