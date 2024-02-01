from lib.fs import *
from lib.api import *
from lib.utils import *
import os
import random

import argparse


# positional arguments:
# num_from_dir  <integer>       number of directories that will be created on client
# num_to_dir    <integer>       number of directories that will be created in OneDrive
def setup_parser(parser):
    parser.add_argument("num_to_dir")


# 0 <= x < max
def random_num(maxr):
    return random.randint(0, int(maxr) - 1)


def main():
    parser = argparse.ArgumentParser()
    setup_parser(parser)
    args = parser.parse_args()

    mapping = {}

    num_to_dir = args.num_to_dir
    test_config = config_get_test()

    token = api_get_token()

    for i in range(0, int(num_to_dir)):
        dirname = test_config["onedrive_dir_prefix"] + str(i)
        print("Creating " + dirname + " on OneDrive")
        #api_create_directory(token, "TestServerBackup", dirname)

    local_dirs = os.listdir(".tmp_test")

    for d in local_dirs:
        mapping[d] = test_config["onedrive_dir_prefix"] + str(random_num(num_to_dir))

    print(mapping)

    user_config = config_get_user()
    root_path = config_get_dev_paths()["repo_path"]

    test_user_pairs = []

    for local_dir in mapping.keys():
        test_user_pairs.append({
            "local_dir": os.path.join(root_path, "test", local_dir),
            "server_dir": test_config["onedrive_root_dir"] + "/" + mapping[local_dir]
        })

    print(test_user_pairs)


if __name__ == '__main__':
    main()
