import json
import os
from typing import Any, Optional

def read_json(filepath:str) -> list | dict:
    f = open(filepath)
    js = json.load(f)
    f.close()
    return js

def write_json(filepath:str, json_obj:list|dict):
    f = open(filepath, 'w')
    json.dump(json_obj, f)
    f.close()

def copy_file(source:str, destination:str, chunk:int = 1024*10):
    with open(source, 'rb') as src, open(destination, 'wb') as dst:
        c = src.read(chunk)
        while c:
            dst.write(c)
            c = src.read(chunk)

def copy_tree(source:str, destination:str):
    os.makedirs(destination)
    listed = os.listdir(source)
    while listed:
        item = listed.pop(0)
        src = os.path.join(source, item)
        dst = os.path.join(destination, item)

        if os.path.isfile(src):
            copy_file(src, dst)
        elif os.path.isdir(src):
            os.makedirs(dst)
            listed.extend(os.listdir(src))


def delete_folder(folder_path:str):
    listed = list(map(lambda x: os.path.join(folder_path, x), os.listdir(folder_path)))
    directories = []
    while listed:
        item = listed.pop(0)
        if os.path.isdir(item):
            listed.extend(map(lambda x: os.path.join(item, x), os.listdir(item)))
            directories.append(item)
        elif os.path.isfile(item) or os.path.islink(item):
            os.unlink(item)
    
    for dir in directories[::-1]:
        os.rmdir(dir)
    os.rmdir(folder_path)

def generate_php_config(filename:str, definitions:dict[str, str] = {}, sdir:bool = False, requirement_files:list[str] = []):
    with open(filename, 'w') as php:
        php.write("<?php\n")
        for fname in requirement_files:
            php.write(f"require_once('{fname}');\n")

        if sdir:
            php.write("$sdir = str_replace('\\\\', '/', __DIR__);\n")

        for key, value in definitions.items():
            php.write(f"define('{key}', {'$sdir.' if sdir else ''}'{value}');\n")

        if sdir:
            php.write("unset($sdir);\n")

def binary_search(lst:list[Any], searchFor:Any, key = lambda x:x):
    llst = len(lst)
    if llst == 1 and key(lst[0]) == searchFor:
        return 0
    elif llst < 2:
        return None
    else:
        ascending = key(lst[0]) < key(lst[-1])

    start = 0
    end = len(lst) - 1
    while start <= end:
        mid = (start + end) // 2
        klm = key(lst[mid])
        if klm == searchFor:
            return mid
        elif klm > searchFor:
            if ascending:
                end = mid - 1
            else:
                start = mid + 1
        else: # klm < searchFor
            if ascending:
                start = mid + 1
            else:
                end = mid - 1

def append_sorted(lst:list[Any], itemToAdd:Any, key = lambda x:x, ascending:Optional[bool] = None):
    if ascending is None:
        if len(lst) < 2:
            ascending = True
        else:
            ascending = key(lst[0]) < key(lst[-1])
    
    keyedItem = key(itemToAdd)
    for i, item in enumerate(lst):
        if ascending != (not (keyedItem < key(item))):
                lst.insert(i, itemToAdd)
                return
    lst.append(itemToAdd)

def remove_subpath(path_:str, subp:str):
    pathl = path_.replace("\\", "/").split('/')
    subpl = subp.replace("\\", "/").split('/')

    while subpl != [] and pathl != [] and subpl[0] == pathl[0]:
        subpl.pop(0)
        pathl.pop(0)
    
    return '/'.join(pathl)