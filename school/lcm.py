from timeit import default_timer as timer


def time(func):
    """timer function"""

    def wrapper(*args):
        start = timer()
        result = func(*args)
        end = timer()
        print(f"function run in {end - start} seconds with result------------------- {result}")

    return wrapper


@time
def lcm(x, y):
    greater = max(x, y)
    while True:
        if greater % x == 0 and greater % y == 0:
            return greater
        greater += 1


@time
def lcm2(x, y):
    greater = max(x, y)
    counter = 1
    while True:
        check = greater * counter
        if check % y == 0 and check % x == 0:
            return check
        counter += 1


a, b = (2133, 22112)

lcm2(a, b)
lcm(a, b)

