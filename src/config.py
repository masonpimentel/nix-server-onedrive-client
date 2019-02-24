from api import *

with open("../config.json") as config_file:
    json_config = json.load(config_file)
    auth = json_config["auth"]


def main():
    # check for auth.auth_code

    # check for auth.client_id and auth.client_secret

    t = api_get_refresh_token()
    print(t)

if __name__ == '__main__':
    main()
