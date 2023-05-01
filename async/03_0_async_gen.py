from collections import deque
from time import sleep


def print_nums():
    num = 1
    while True:
        print(num)
        num += 1
        yield


def print_time():
    count = 0
    while True:
        if count % 3 == 0:
            print(f'{count} seconds have passed')
        count += 1
        yield


def main():
    g1 = print_nums()
    g2 = print_time()
    queue = deque([g1, g2])

    while True:
        g = queue.popleft()
        next(g)
        queue.append(g)
        sleep(0.2)


if __name__ == '__main__':
    main()
