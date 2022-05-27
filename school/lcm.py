import threading
from timeit import default_timer as timer


def time(func):
    def wrapper(*args):
        """timer function"""
        start = timer()
        result = func(*args)
        end = timer()
        print(f"function run in {end - start} seconds with result: {result}")

    return wrapper


@time
def calculate_lcm(x, y):
    greater = max(x, y)
    while True:
        if greater % x == 0 and greater % y == 0:
            return greater
        greater += 1


@time
def calculate_lcm2(x, y):
    greater = max(x, y)

    counter = 1
    while True:
        check = greater * counter
        if check % y == 0 and check % x == 0:
            return check
        counter += 1


if __name__ == '__main__':
    a, b = (2133, 22112)

    th1 = threading.Thread(target=calculate_lcm, args=(a, b))
    th2 = threading.Thread(target=calculate_lcm2, args=(a, b))
    th1.start()
    th2.start()

