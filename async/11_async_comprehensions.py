import asyncio

from faker import Faker

faker = Faker('en_US')

# асихронный генератор
async def get_user(n=1):
    await asyncio.sleep(1)
    for i in range(n):
        name, surname = faker.name_male().split()
        yield name, surname


async def main():
    l = [name async for name in get_user(3)]
    print(l)

    d = {name: surname async for name, surname in get_user(3)}
    print(d)


if __name__ == '__main__':
    asyncio.run(main())
