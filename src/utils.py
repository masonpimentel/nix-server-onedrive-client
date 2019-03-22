import json


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
