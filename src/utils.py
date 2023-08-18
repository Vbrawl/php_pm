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

def copy_tree(source:str, destination:str, exceptions:list[str|list[str]] = []): # type: ignore
    exceptions:list[list[str]] = list(map(lambda x: parts_in_path(x) if isinstance(x, str) else x, exceptions))

    os.makedirs(destination)
    listed = os.listdir(source)
    while listed:
        item = listed.pop(0)
        item_parts = parts_in_path(item)

        is_exceptional = False
        for exception in exceptions:
            if item_parts[-len(exception):] == exception:
                is_exceptional = True
        if is_exceptional:
            continue


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
            php.write("$sdir = str_replace('\\\\', '/', __DIR__).'/';\n")

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

def remove_common_path(*all_paths:str|list[str], join:bool = True):
    paths = []
    for path in all_paths:
        if isinstance(path, str):
            paths.append(parts_in_path(path))
        else:
            paths.append(path)

    slice_parts = 0
    for i in range(len(paths[0])):
        part = paths[0][i]
        failure = False
        for path in paths:
            if path[i] != part:
                failure = True
                break
        if failure:
            break
        else:
            slice_parts = i + 1
    
    if join:
        return tuple(map(lambda x: '/'.join(x[slice_parts:]), paths))
    else:
        return tuple(map(lambda x: x[slice_parts:], paths))

def parts_in_path(path:str):
    res = path.replace('\\', '/').split('/')
    for i in range(res.count("")):
        res.remove("")
    return res