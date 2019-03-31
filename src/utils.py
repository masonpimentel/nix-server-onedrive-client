import json
from debugging import *


def config_get_dev():
    with open("../dev_config.json") as config_file:
        return json.load(config_file)


def config_get_user():
    with open("../user_config.json") as config_file:
        return json.load(config_file)


def config_get_dev_urls():
    return config_get_dev()["urls"]


def config_get_dev_auth():
    return config_get_dev()["auth"]


def config_get_user_auth():
    return config_get_user()["auth"]


def config_get_dev_req_bodies():
    return config_get_dev()["req_bodies"]


def config_get_dev_paths():
    return config_get_dev()["paths"]


def config_get_user_paths():
    return config_get_user()["paths"]


def config_get_user_limits():
    return config_get_user()["limits"]


def config_get_user_verbosity():
    return config_get_user()["verbosity"]


def config_write_dev(new_config):
    with open("../dev_config.json", "w") as config_file:
        json.dump(new_config, config_file, indent=4, sort_keys=True)


def config_clear_dev_auth_code():
    dev_config = config_get_dev()
    dev_config["auth"]["auth_code"] = ""
    config_write_dev(dev_config)

