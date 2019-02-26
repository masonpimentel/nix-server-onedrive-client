import json


def config_get_root():
    with open("../config.json") as config_file:
        return json.load(config_file)


def config_get_urls():
    return config_get_root()["urls"]


def config_get_auth():
    return config_get_root()["auth"]


def config_get_req_bodies():
    return config_get_root()["req_bodies"]
