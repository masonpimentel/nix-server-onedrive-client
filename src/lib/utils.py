import json


def config_get_dev():
    with open("../dev_config.json") as config_file:
        return json.load(config_file)


def config_get_user():
    with open("../user_config.json") as config_file:
        return json.load(config_file)


def config_get_test():
    with open("../test/test_config.json") as config_file:
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


def config_write_user(new_config):
    with open("../user_config.json", "w") as config_file:
        json.dump(new_config, config_file, indent=4, sort_keys=True)


def config_clear_dev_auth_code():
    dev_config = config_get_dev()
    dev_config["auth"]["auth_code"] = ""
    config_write_dev(dev_config)


def config_clear_refresh_token():
    dev_config = config_get_dev()
    dev_config["auth"]["refresh_token"] = ""
    dev_config["req_bodies"]["refresh_body"] = ""
    config_write_dev(dev_config)


def config_clear_user_auth():
    user_config = config_get_user()
    user_config["auth"]["client_id"] = ""
    user_config["auth"]["client_secret"] = ""
    config_write_user(user_config)


def config_replace_cronjob_line(find_string, replace_string_with, contains=False):
    f = open("../cronjob", "r")
    lines = f.readlines()
    f.close()

    for i, line in enumerate(lines):
        if (contains and find_string in line) or (line.rstrip("\n") == find_string):
            lines[i] = replace_string_with + "\n"
            f = open("../cronjob", "w")
            contents = "".join(lines)
            f.write(contents)
            f.close()
            return True

    return False


def config_clear_cronjob_repo_path():
    config_replace_cronjob_line("repo_path=", "{repo_path_cmd}", True)
