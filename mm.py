#!/usr/bin/env python3
# -*- coding: utf-8 -*-

criteria = '"address":"(0x[0-9a-fA-F]{40})"'

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
        return []
    
    text = str(file_content).replace('\n', '')
    idx = text.find("identities")
    if idx == -1:
        print(f"# No identities: {file_path}")
    
    id_text = text[idx:]

    # find items
    pattern = re.compile(criteria)
    ret = re.findall(pattern, id_text)

    # removing duplicate items
    ret = list(set(ret))

    # print items
    for r in ret:
        print(r)
    
    return ret


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
