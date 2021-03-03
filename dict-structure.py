# This file contains a function to combine key-value pairs
# extracted from sections of text with their respective
# section headers
#
# Author(s): Maja Minnaert

import json

def create_skeleton_dict(headers, keyvals):
    """Makes nested dict based on list and dict or list
    *currently only supports one level down of nesting*

    Parameters: a list of headers and a list of dicts where
    the lists are of equal length (the length of the dicts
    can vary without causing issue).

    Returns: a nested dictionary where respective 'keyvals' are
    nested in respective 'headers' based on order in the list
    and dictionary provided as parameters
    """
    data = dict(zip(headers, keyvals))
    with open("data.json", "w") as write_file:
        json.dump(data, write_file, indent=4)
    return data


if __name__ == "__main__":
    header_list = ["header1", "header2", "header3", "header4"]
    keyval_list = [{"key1.1": "val1.1", "key1.2": "val1.2", "key1.3": "val1.3"},
                   {"key2.1": "val2.1", "key2.2": "val2.2", "key2.3": "val2.3"},
                   {"key3.1": "val3.1", "key3.2": "val3.2", "key3.3": "val3.3"},
                   "value4"]
    dict_demo = create_skeleton_dict(header_list, keyval_list)
    print(dict_demo)
    print(type(dict_demo)) # Have a look at the json file in the folder of this script also
