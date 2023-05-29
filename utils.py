
from datetime import datetime
import importlib
import json
import logging
from typing import Iterable, Union


def reload_lib(lib):
    importlib.reload(lib)


def get_timestamp():
    return datetime.now().isoformat(timespec='seconds').replace(':', '_')

def get_timestamp_name(name, directory, ext="json"):
    now = get_timestamp()
    name = f"{directory}/{name}_{now}.{ext}"
    return name


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
        timestamp_directory,
    ):
        self.directory = directory
        self.timestamp_directory = timestamp_directory

    def write(self, obj, name, timestamp: Union[str, bool] = False, json_write=False):
        ext = "log"
        if json_write:
            ext = "json"

        if timestamp:
            d = self.timestamp_directory if self.timestamp_directory is not None else directory
            if isinstance(timestamp, str):
                name = f"{d}/{name}-{timestamp}.{ext}"
            else:
                name = get_timestamp_name(name, directory=d, ext=ext)
        else:
            name = f"{self.directory}/{name}.{ext}"

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