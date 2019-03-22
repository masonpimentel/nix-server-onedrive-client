import os
from debugging import *
from utils import *


def fs_get_local_filename():
    paths = config_get_dev_paths()
    return os.path.basename(paths["upload_pairs"][0])


def fs_get_filename(filename):
    return os.path.basename(filename)


def fs_get_upload_size():
    paths = config_get_dev_paths()
    try:
        size = os.stat(paths["upload_pairs"][0]).st_size
    except FileNotFoundError:
        print_message("File '" + paths["upload_pairs"][0] + "' could not be found!", "UPLOAD", "error")
        return None
    return size


def fs_get_chunk_size(filename):
    return os.stat(filename).st_size


def fs_get_parent_dir():
    return os.path.dirname(os.getcwd())


def fs_get_chunk_full_path(tmpdirname, chunk_name):
    return os.path.join(tmpdirname, chunk_name)
