import copy
import os
import logging
import functools
import random
import time

logger = logging.getLogger(__name__)
time_logger = logging.getLogger('timing')

import pyarrow as pa

def timeit(func):
    """
    A decorator that measures and logs the execution time of a function.

    Parameters
    ----------
    func : function
        The function whose execution time is to be measured.

    Returns
    -------
    function
        The wrapped function with timing capabilities.

    Example
    -------
    @timeit
    def example_function():
        # Function logic here
        pass
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        time_logger.debug(f"Function {func.__name__!r} executed in {elapsed_time:.4f} seconds")
        return result

    return wrapper


def is_directory_empty(directory_path:str):
    """
    Checks if a given directory is empty.

    Parameters
    ----------
    directory_path : str
        The path to the directory to check.

    Returns
    -------
    bool
        True if the directory is empty, False otherwise.

    Example
    -------
    >>> is_empty = is_directory_empty('/path/to/directory')
    True
    """

    return not os.listdir(directory_path)


def is_contained(list1, list2):
    """
    Checks if all elements of the first list are contained in the second list.

    Parameters
    ----------
    list1 : list
        The list whose elements are to be checked.
    list2 : list
        The list in which to check for the presence of `list1` elements.

    Returns
    -------
    bool
        True if all elements of `list1` are contained in `list2`, False otherwise.

    Example
    -------
    >>> is_contained([1, 2], [1, 2, 3, 4])
    True
    """
    return set(list1).issubset(set(list2))



def generate_similar_data(template_data, num_entries):
    """
    Generates new data entries based on the structure and values of a template dataset.

    Parameters
    ----------
    template_data : list of dict
        A list of dictionaries containing the template data to base new entries on.
    num_entries : int
        The number of similar data entries to generate.

    Returns
    -------
    list of dict
        A list of generated data entries with variations in the values.

    Example
    -------
    >>> template = [{'id': 0, 'value': 10, 'name': 'item'}]
    >>> new_data = generate_similar_data(template, 5)
    >>> print(new_data)
    [{'id': 0, 'value': 9, 'name': 'item_5'}, {'id': 1, 'value': 11, 'name': 'item_89'}, ...]
    """
    def generate_value(value):
        if isinstance(value, int):
            return random.randint(value - 10, value + 10)
        elif isinstance(value, float):
            return round(random.uniform(value * 0.8, value * 1.2), 2)
        elif isinstance(value, str):
            return f"{value}_{random.randint(1, 100)}"
        elif isinstance(value, dict):
            return {k: generate_value(v) for k, v in value.items()}
        # elif isinstance(value, list):
        #     return [generate_value(item) for item in value]
        elif value is None:
            return None
        else:
            return value

    generated_data = []
    for i in range(num_entries):
        new_entry = copy.deepcopy(random.choice(template_data))
        for key, value in new_entry.items():
            if key == 'id':
                new_entry[key] = i
            else:
                new_entry[key] = generate_value(value)
        generated_data.append(new_entry)

    return generated_data