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
            try:
                command = 'tell app "Finder" to empty'
                p = Popen(
                    ["osascript", "-"], stdin=PIPE, stdout=PIPE, universal_newlines=True
                )
                stdout, stderr = p.communicate(command)
                print("Trash is empty")
            except Exception as e:
                print(e)
                print("trash is already empty")
    else:
        clean_system_trash()
