import yaml
import pandas as pd
import sys


# flatten each dict even further and prevent dict keys from showing up
def flatten_dict(d):
    out = {}
    d = pd.json_normalize(d, sep='/').to_dict(orient='records')[0]

    for key, values in d.items():
        if type(values) is dict:
            sys.exit(f"Error: Lowest level children cannot be a list of dicts: {values}")
        elif type(values) is list:
            for value in values:
                if type(value) is dict:
                    sys.exit(f"Error: Lowest level children cannot be a list of dicts: {values}")
                else:
                    out.setdefault(key, []).append(value)
        elif type(values) is str:
            out.setdefault(key, []).append(values)
    return out


def diff_yaml_files(old, new):
    # open each yaml file and load into a dict
    with open('d-old.yaml') as f:
        d_old = yaml.load(f, Loader=yaml.FullLoader)

    with open('d-new.yaml') as f:
        d_new = yaml.load(f, Loader=yaml.FullLoader)

    # flatten each dict down to its keys and a "/" separator between subpaths
    d_old_flat = flatten_dict(d_old)
    d_new_flat = flatten_dict(d_new)

    # find what has been added to the new file
    adds = {}
    for path, values in d_new_flat.items():
        if path in d_old_flat.keys():
            added_items = list(set(values) - set(d_old_flat[path]))
            if added_items:
                for item in added_items:
                    adds.setdefault(path, []).append(item)
        else:  # this is a newly added item
            for item in values:
                adds.setdefault(path, []).append(item)

    # find what has been removed from the original file
    deletes = {}
    for path, values in d_old_flat.items():
        if path in d_new_flat.keys():
            removed_items = list(set(values) - set(d_new_flat[path]))
            if removed_items:
                for item in removed_items:
                    deletes.setdefault(path, []).append(item)
        else:  # this is a newly added item
            for item in values:
                deletes.setdefault(path, []).append(item)

    return {"adds": adds, "deletes": deletes}


diff = diff_yaml_files("d-old.yaml", "d-new.yaml")
print(diff)
