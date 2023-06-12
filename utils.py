
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


from dataclasses import dataclass
from typing import Dict

class Buildable:
    """
    So you can build classes by defining just their name.
    ## Example
    ```python
    transitions = {
        {'name': 'linear', 'kwargs': {}}
    }
    for t in transitions:
        built_transition = Transition.build(**t)

    class Transition(Buildable):
        ...
    class Transition_linear:
        ...
    class Transition_bezier:
        ...

    Transition.register_classes({
        'Transition_linear': Transition_linear,
        'Transition_bezier': Transition_bezier,
    })
    ```
    """
    classes: Dict[str, type] | None = None

    @classmethod
    def register_classes(cls, classes_dict):
        if not cls.classes:
            cls.classes = {}
        cls.classes = {**cls.classes, **classes_dict}

    @classmethod
    def set_classes(cls, classes_dict):
        cls.classes = classes_dict

    @classmethod
    def build(cls, name, **kwargs):
        if not cls.classes:
            raise NotImplementedError("")
        class_name = cls.__name__
        c = cls.classes[f"{class_name}_{name}"]
        if c:
            return c(**kwargs)
        raise NotImplementedError()

    def getName(self):
        class_name = '_'.join(self.__class__.__name__.split('_')[1:])
        return class_name


import time
from dataclasses import dataclass

@dataclass
class Cooldown:
    seconds: float = 0.0
    start: float = 0.0

    def isStarted(self):
        return self.start != 0
    
    def clear(self):
        self.start = 0

    def trigger(self, time_counter=None, check=True):
        triggered = 0
        if not time_counter:
            time_counter = time.perf_counter()
        if check:
            triggered = self.check(time_counter)
            if triggered < 1:
                return triggered
        self.start = time_counter
        self.end = time_counter + self.seconds
        return triggered

    def elapsed(self, time_counter = None):
        if not time_counter:
            time_counter = time.perf_counter()
        if self.start == 0.0:
            return 0.0, time_counter
        elapsed  = time_counter - self.start
        return elapsed, time_counter

    def check(self, time_counter = None):
        # returns how many triggers happened
        elapsed, _  = self.elapsed(time_counter)
        return (elapsed / self.seconds)
    
    def getEnd(self):
        return  self.start + self.seconds
    
    def to_end(self, time_counter = None):
        if not time_counter:
            time_counter = time.perf_counter()
        elapsed, _  = self.elapsed(time_counter)
        return  self.seconds - elapsed


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
