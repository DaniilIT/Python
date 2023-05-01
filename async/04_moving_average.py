# декоратор, чтобы не писать при старте g.send(None)
def init_gen(func):
    def inner(*args, **kwargs):
        g = func(*args, **kwargs)
        g.send(None)
        return g

    return inner


@init_gen
def moving_average():  # скользящее среднее
    count = 0
    summ = 0
    average = None

    while True:
        try:
            x = yield average
        except StopIteration:
            print('Done!')
            break
        else:
            count += 1
            summ += x
            average = round(summ / count, 2)

    return average


g = moving_average()
print(g.send(25))  # 25.0
print(g.send(1))  # 13.0
try:
    g.throw(StopIteration)  # Done!
except StopIteration as e:
    print('Average: ', e.value)  # Average 13.0
