
from datetime import datetime
import importlib
import json
import logging
import os
from typing import Iterable, Union


def reload_lib(lib):
    importlib.reload(lib)


def get_timestamp():
    return datetime.now().isoformat(timespec='seconds').replace(':', '_')

def get_timestamp_filename(name, directory, ext="json", timestamp=None, format="{directory}/{name}_{timestamp}.{ext}"):
    if not isinstance(timestamp, str):
        timestamp = get_timestamp()
    filename = f"{directory}/{name}_{timestamp}.{ext}".format(
        directory=directory,
        name=name,
        timestamp=timestamp,
        ext=ext,
    )
    return filename


def string_parameters(parameters):
    return " ".join([f" {k}_{parameters[k]}" for k in parameters.keys()])

def is_float(string):
    try:
        float(string)
        return True
    except ValueError:
        return False

def save_to_json(dict, filename):
  with open(filename, 'w') as f:
      json.dump(dict, f, indent=4)




class FileWriter:
    def __init__(self,
        directory,
        directory_timestamped,
    ):
        self.directory = directory
        self.directory_timestamped = directory_timestamped

    def write(self, obj, name, timestamp: Union[str, bool] = False, json_write=False):
        ext = "log"
        if json_write:
            ext = "json"

        d = self.directory
        if timestamp:
            d = self.directory_timestamped if self.directory_timestamped is not None else self.directory
            name = get_timestamp_filename(
                name, directory=d, ext=ext, timestamp=timestamp)
        else:
            name = f"{d}/{name}.{ext}"
        os.makedirs(d, exist_ok=True)
        with open(name, mode="w", encoding="utf-8") as f:
            if json_write:
                json.dump(obj, f, ensure_ascii=False, indent=2)
            else:
                if isinstance(obj, Iterable):
                    for o in obj:
                        try:
                            f.write(str(o) + "\n\n")
                        except Exception as e:
                            logging.exception("write error")
                else:
                    try:
                        f.write(str(obj))
                    except:
                        pass



def binary_search(minimum, maximum, func):
    mi, ma = minimum, maximum
    while minimum <= maximum:
        mid = (minimum + maximum) // 2
        if func(mid):
            maximum = mid - 1
        else:
            minimum = mid + 1
    return max(mi, min(ma, minimum))


def text_lines_collate(a, b):
    a_list = a.split('\n')
    b_list = b.split('\n')
    output_list = []
    for i in range(len(a_list)):
        output_list.append(a_list[i])
        output_list.append(b_list[i])
    return '\n'.join(output_list)
