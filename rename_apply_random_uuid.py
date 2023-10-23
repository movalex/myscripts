import uuid
import os
import sys

EXT_LIST = [".jpg"]


def rename_file(path):
    path = os.path.abspath(path)
    print("Renaming...")
    count = 0
    for file_name in os.listdir(path):
        full_path = os.path.join(path, file_name)
        if os.path.isfile(full_path):
            name, ext = os.path.splitext(file_name)
            if ext in EXT_LIST:
                count += 1
                new_name = os.path.join(path, create_uuid(ext))
                os.rename(full_path, new_name)
    print("Done!")
    if count:
        print(f"renamed files: {count}")


def create_uuid(ext):
    rand = str(uuid.uuid4()) + ext
    return rand


if __name__ == "__main__":

    if len(sys.argv) == 2:
        path = sys.argv[1]
        if os.path.isdir(path):
            rename_file(path)
