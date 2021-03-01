# This file contains the skeleton of the dictionary
# You can use this skeleton to store the extracted values
# for each of the key's, there should be space for each of
# the key's that can be extracted from the provided pdf files

# This is a work in progress
# Todo: investigate option of homemade object
# Todo: find way to automate for more than 3 levels


def create_skeleton_dict(headers :list, keyvals :dict):
    """Makes nested dict based on list and dict or list
    *currently only supports one level down of nesting*

    Parameters: a list and a dict, where the list is top level
    headers and the subsequent dict consists of keys and values
    of the to be nested dict

    Returns: a nested dictionary where respective 'keyvals' are
    nested in respective 'headers' based on order in the list
    and dictionary provided as parameters
    """
    skeleton_dict = dict(zip(headers, keyvals))
    return skeleton_dict
