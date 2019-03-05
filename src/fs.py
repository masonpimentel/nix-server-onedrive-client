import os
from debugging import *
from utils import *


def fs_get_local_filename():
    paths = config_get_paths()
    return os.path.basename(paths["upload_pairs"][0]["local_dir"])


def fs_get_filename(filename):
    return os.path.basename(filename)


def fs_get_upload_size():
    paths = config_get_paths()
    try:
        size = os.stat(paths["upload_pairs"][0]["local_dir"]).st_size
    except FileNotFoundError:
        print_message("File '" + paths["upload_pairs"][0]["local_dir"] + "' could not be found!", "UPLOAD", "error")
        return None
    return size


def fs_get_chunk_size(filename):
    return os.stat(filename).st_size
