from api import *
import json

with open("../config.json") as e_config_file:
    json_config = json.load(e_config_file)
    auth = json_config["auth"]


def main():
    # check for auth.auth_code

    # check for auth.client_id and auth.client_secret

    refresh_token = api_get_refresh_token()
    if refresh_token is not None:
        json_config["auth"]["refresh_body"] = refresh_token
        with open("../config.json", "w") as config_file:
            json.dump(json_config, config_file, indent=4, sort_keys=True)
            print_message("Successfully set up refresh token!", "CONFIG", "info")

if __name__ == '__main__':
    main()
