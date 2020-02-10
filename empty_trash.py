#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# delete trash files on MacOS

import os
import sys
from pathlib import Path
from subprocess import Popen, PIPE


def clean_system_trash():
    trash = Path("~/.Trash").expanduser()
    os.chdir(str(trash))
    if not os.listdir():
        print("system trash is empty")
    else:
        os.system("rm -rf *")
        print("done!")


if __name__ == "__main__":
    if len(sys.argv) >= 2:
        if sys.argv[1] == "-d":
            command = 'tell app "Finder" to empty'
            p = Popen(
                ["osascript", "-"], stdin=PIPE, stdout=PIPE, stderr=PIPE, universal_newlines=True
            )
            stdout, stderr = p.communicate(command)
            if p.returncode == 0:
                print('Trash is empty')
            else:
                print('trash is already empty, cancelling')
        elif sys.argv[1] == "-h":
                print("Help:\nUse '-d' to delete Trash files from all disks")
    else:
        clean_system_trash()
