#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os
import re
import sys
import glob
import json
import datetime


# Save as a file
def save_file(text, filename="test.htm"):
    if type(text) != "str":
        text = str(text)
    file = open(filename, "w", encoding="utf-8")
    file.write(text)
    file.close()


# Append as a file
def append_file(text, filename="output.txt"):
    if type(text) != "str":
        text = str(text)
    file = open(filename, "a", encoding="utf-8")
    file.write(text)
    file.close()


# Read file
def read_file(filename="test.htm"):
    file = open(filename, "r", encoding="utf-8")
    text = file.read()
    file.close()
    return text


# Save as json
def save_json_file(json_value, file_path):
    with open(file_path, "a") as file:
        # Write the JSON data to the file
        json.dump(json_value, file)


def check_file(file_path):
    try:
        file = open(file_path, "rb")
        text = file.read()
        file.close()
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return []

    if text == "":
        return []

    # find items
    criteria = '"0x[0-9a-fA-F]{40}":\{"address":"(0x[0-9a-fA-F]{40})","([^a][^"]*)"'
    pattern = re.compile(criteria)
    result = re.findall(pattern, str(text).replace("\n", ""))

    # tidy
    ret = []
    for row in result:
        if row[1] != 'decimals' and row[1] != 'aggregators' and row[1] != 'chainId':
            ret.append(row[0])
            print(f"{file_path}:", row)
    return ret


def check_all(ttf_path):
    ret = []
    if os.path.isdir(ttf_path):
        for file_path in glob.glob(ttf_path + os.sep + "*"):
            ret.extend(check_all(file_path))
    else:
        if os.path.isfile(ttf_path):
            ret.extend(check_file(ttf_path))

    # removing duplicate items
    ret = list(set(ret))
    return ret


# check arguments
if len(sys.argv) != 2:
    print(f"Usage: {os.path.basename(sys.argv[0])} <dir>")
    sys.exit(1)

all_ret = check_all(sys.argv[1])

# print items
timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
output_file = f"addr_{timestamp}.txt"
for addr in all_ret:
    append_file(f"{addr}\n", output_file)
print(f"Total: {len(all_ret)}")
