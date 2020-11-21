import os
import json
import numpy as np

def determine_filepath(dir_name: str, label: str) -> str:
    save_dir = dir_name + '/' + label
    os.makedirs(save_dir, exist_ok=True)

    all_files = os.listdir(save_dir)
    number = 0

    if any(all_files):
        with_label = list(filter(lambda x: x.startswith(label), all_files))
        numbers = list(map(lambda x: int(x.split(label)[1].split('.')[0]), with_label))
        number = max(numbers) + 1

    return save_dir + '/' + label + str(number) + '.json'


def save_to_json(filename: str, data):
    with open(filename, 'w') as file:
        json.dump(data, file)


def from_json(filename:str):
    with open(filename, 'r') as file:
        return np.array(json.loads(file.read()))