import os
import json

with open("../config.json") as config_file:
    json_config = json.load(config_file)
    UPLOAD_PATHS = json_config["paths"]["upload"]

def fs_get_filename():
    return os.path.basename(UPLOAD_PATHS[0])


def fs_get_upload_size():
    return os.stat(UPLOAD_PATHS[0]).st_size


def fs_get_chunk_size(filename):
    return os.stat(filename).st_size
