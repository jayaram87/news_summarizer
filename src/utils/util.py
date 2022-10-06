import os
import sys
import yaml
import json
import pickle

def read_yaml(file_path: str) -> dict:
    try:
        with open(file_path, 'rb') as f:
            file = yaml.safe_load(f)
        return file
    except Exception as e:
        print(str(e))

def save_object(file_path: str, object):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, 'wb') as f:
            pickle.dump(object, f)
    except Exception as e:
        print(str(e))


