class MyException(Exception):
    pass


def subgen():
    while True:
        try:
            message = yield
            print('message: ', message)
        except MyException:
            print('Done!')
        except StopIteration:
            break

    return 'Returned from subject()'


def init_gen(func):
    def inner(*args, **kwargs):
        g = func(*args, **kwargs)
        g.send(None)
        return g

    return inner


@init_gen
def delegator(g):
    result = yield from g  # в других языках - await
    print('result', result)


sg = subgen()
g = delegator(sg)

g.send('test')  # message: test
g.throw(MyException)  # Done!
g.send('test')  # message: test
try:
    g.throw(StopIteration)  # result Returned from subject()
except StopIteration:
    pass
