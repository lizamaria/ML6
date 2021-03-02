# This file contains the skeleton of the dictionary
# You can use this skeleton to store the extracted values
# for each of the key's, there should be space for each of
# the key's that can be extracted from the provided pdf files

# This is a work in progress
# Currently tested for list of headers and list of key-value dicts
# that correspond by order in the respective lists
# Todo: find way to extend a level of the tree (currently checking conversion dict -> list of dicts approach)


def create_skeleton_dict(headers: list, keyvals: list):
    """Makes nested dict based on list and dict or list
    *currently only supports one level down of nesting*

    Parameters: a list of headers and a list of dicts of equal length

    Returns: a nested dictionary where respective 'keyvals' are
    nested in respective 'headers' based on order in the list
    and dictionary provided as parameters
    """
    skeleton_dict = dict(zip(headers, keyvals))
    skeleton_dict = skeleton_dict.items()
    return skeleton_dict


if __name__ == "__main__":
    header_list = ["header1", "header2", "header3"]
    keyval_list = [{"key1": "val1", "key2": "val2", "key3": "val3"},
                   {"key1": "val1", "key2": "val2", "key3": "val3"},
                   {"key1": "val1", "key2": "val2", "key3": "val3"}]
    print(create_skeleton_dict(header_list, keyval_list))
    print(create_skeleton_dict(header_list, keyval_list))
    print(type(create_skeleton_dict(header_list, keyval_list)))
