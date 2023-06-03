
import logging

loggingDefaultFormat = '%(asctime)s %(levelname)s %(filename)s:%(lineno)d(%(process)d) `"%(message)s"`'
loggingDefaultFormatter = logging.Formatter(loggingDefaultFormat)

def loggingSetFormatter(fh_formatter = loggingDefaultFormatter):        
    fh = logging.StreamHandler()
    fh.setFormatter(fh_formatter)

def loggingGetLogger(name, fh = logging.StreamHandler(), fh_formatter = loggingDefaultFormatter):
    logger = logging.getLogger(name)
    fh.setFormatter(fh_formatter)
    logger.addHandler(fh)
    return logger

# logger = loggingGetLogger(__name__)
# logger.setLevel('WARN')

from datetime import datetime
import importlib
import json
import os
import re
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

    def write(self, obj, name, timestamp: Union[str, bool] = False, json_write=False, raise_exception=True):
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
                    exceptions = []
                    for o in obj:
                        try:
                            f.write(str(o) + "\n\n")
                        except Exception as e:
                            exceptions.append(e)
                    if exceptions:
                        if raise_exception:
                            raise Exception(exceptions)
                else:
                    try:
                        f.write(str(obj))
                    except:
                        if raise_exception:
                            raise



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


def camel_case_to_spaces(text):
    # Use regular expression to split camel case words
    spaced_text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)
    # Convert to lowercase and remove leading/trailing spaces
    spaced_text = spaced_text.lower().strip()
    return spaced_text

def merge_dictionaries(*dicts):
    """
    N dictionaries, some values are defined, some are "None".
    merge these directories **recursively**, giving priority to later ones.
    """
    result = {}
    for dictionary in dicts:
        for key, value in dictionary.items():
            if isinstance(value, dict) and key in result and isinstance(result[key], dict):
                result[key] = merge_dictionaries(result[key], value)
            else:
                result[key] = value
    return result


def dict_diff(dicts):
    diff = {}
    keys = set()
    for d in dicts:
        keys |= set(d.keys())

    for key in keys:
        values = set()
        for d in dicts:
            val = d.get(key)
            if val is not None:
                values.add(val)
        if len(values) > 1:
            diff[key] = values
    return diff
