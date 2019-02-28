import os
import json

from utils import *

# with open("../config.json") as e_config_file:
#     e_json_config = json.load(e_config_file)
#     UPLOAD_PATHS = e_json_config["paths"]["upload"]

# TODO FIX
UPLOAD_PATHS = ["0"]

def fs_get_local_filename():
    paths = config_get_paths()
    return os.path.basename(paths["upload_pairs"][0]["local_dir"])


def fs_get_filename(filename):
    return os.path.basename(filename)


def fs_get_upload_size():
    return os.stat(UPLOAD_PATHS[0]).st_size


def fs_get_chunk_size(filename):
    return os.stat(filename).st_size
