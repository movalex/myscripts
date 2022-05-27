from timeit import default_timer as timer
from functools import wraps


def time(func):
    @wraps(func)
    def wrapper(*args):
        """timer function"""
        start = timer()
        result = func(*args)
        end = timer()
        print(f"function run in {end - start} seconds with result: {result}")

    return wrapper


@time
def lcm(x, y):
    """get least common multiple"""
    greater = max(x, y)
    counter = 1
    while True:
        check = greater * counter
        if check % y == 0 and check % x == 0:
            return check
        counter += 1

# test:
# a, b = (2133, 22112)
#
# lcm(a, b)
