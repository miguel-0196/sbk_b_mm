#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys
import glob

def check_file(file_path):
    try:
        file = open(file_path, "rb")
        file_content = file.read()
        file.close()
    except FileNotFoundError:
        print(f"# File not found: {file_path}")
        return []

    if file_content == '':
        print(file_path)
    
    text = str(file_content).replace('\n', '')
    idx = text.find("identities")
    if idx == -1:
        print(file_path)
    
    return []


def check_all(ttf_path):
    if os.path.isdir(ttf_path):
        for file_path in glob.glob(ttf_path + os.sep +"*"):
            check_all(file_path)
    else:
        if os.path.isfile(ttf_path) and ttf_path[-4:] == '.log':
            check_file(ttf_path)


# check arguments
if len(sys.argv) != 2:
    print(f"Usage: {os.path.basename(sys.argv[0])} <dir_path>")
    sys.exit(1)

check_all(sys.argv[1])
