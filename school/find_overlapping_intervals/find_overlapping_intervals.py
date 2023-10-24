import csv
from pathlib import Path
from datetime import datetime
from pprint import pprint


def convert_to_time(text: str) -> datetime:
    fmt = "%H:%M"
    return datetime.combine(today, datetime.strptime(text, fmt).time())


def process(intervals: list) -> list:
    """intervals must be sorted by the end time.
    alternatively use
    intervals.sort(key=lambda x: x[2])
    """

    to_delete = []
    if not intervals:
        return 0

    counter = 0  # count how many items to delete
    prev_end = convert_to_time("00:00") # first element is the smallest value, here 00:00
    for row in intervals:
        idx, start, end = row
        start_time = convert_to_time(start)
        end_time = convert_to_time(end)
        # compare start interval with previosu known end interval
        if start_time >= prev_end:
            prev_end = end_time
        else:
            counter += 1
            to_delete.append(row)
    return set(intervals).difference(to_delete)


if __name__ == "__main__":
    today = datetime.today()
    intervals = []
    csv_file = Path("data.csv")

    with open(csv_file.as_posix(), newline="") as file:
        reader = csv.reader(file, delimiter=";")
        next(reader)  # skip header row
        for row in reader:
            intervals.append(tuple(row))

    p = process(intervals)
    pprint(sorted(p, key=lambda x: x[1]))


"""
[('249', '10:05', '10:31'),
 ('799', '10:34', '11:01'),
 ('640', '11:09', '11:40'),
 ('804', '11:47', '12:18'),
 ('296', '12:21', '13:11'),
 ('512', '13:14', '13:46'),
 ('468', '13:52', '14:27'),
 ('876', '14:27', '14:52'),
 ('915', '14:57', '15:35'),
 ('523', '15:38', '16:04'),
 ('855', '16:05', '16:42'),
 ('777', '16:44', '17:17'),
 ('819', '17:17', '17:55')]
"""
