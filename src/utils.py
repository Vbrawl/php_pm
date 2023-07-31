import json
import os

def read_json(filepath:str) -> list | dict:
    f = open(filepath)
    js = json.load(f)
    f.close()
    return js

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