import sys

JUMP = [5, -3]
direction = sum(JUMP)


def hop(target):
    pos = 0
    counter = 0
    while True:
        pos += JUMP[0]
        print(pos)
        counter += 1
        if target == pos:
            print(f"hopped in {counter} jumps")
            return
        pos += JUMP[1]
        print(pos)
        counter += 1
        if pos == target:
            print(f"hopped in {counter} jumps")
            return
        if direction > 0:
            if pos > target + max(JUMP):
                break
        else:
            if pos < target + min(JUMP):
                break
    print("кузнечик не допрыгает")


if __name__ == "__main__":
    hop(int(sys.argv[1]))
