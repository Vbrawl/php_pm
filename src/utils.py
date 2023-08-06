import json
import os

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

def generate_php_config(filename:str, definitions:dict[str, str]):
    with open(filename, 'w') as php:
        php.write("<?php")
        for key, value in definitions.items():
            php.write(f'\ndefine("{key}", "{value}");')