from lib.api import *
from lib.utils import *

import argparse


def setup_parser(parser):
    parser.add_argument("--clear", action="store_true", help="clear configuration including client id, client secret and refresh token")


def clear_configuration():
    config_clear_user_auth()
    config_clear_dev_auth_code()
    config_clear_refresh_token()
    print_message("Configuration has been cleared! Re-enter your client ID, client secret in user_config.json to re-configure", "CONFIG", "info")


def setup_refresh_token():
    dev_config = config_get_dev()
    dev_auth = config_get_dev_auth()
    dev_urls = config_get_dev_urls()
    dev_req_bodies = config_get_dev_req_bodies()
    user_auth = config_get_user_auth()

    if not dev_req_bodies["refresh_body"]:
        if user_auth["client_id"] == "fill_me_in" or user_auth["client_secret"] == "fill_me_in":
            # TODO add section
            print_message("Client auth info not added to config. Please refer to TODO", "CONFIG", "error")
            return
        if not dev_auth["auth_code"]:
            print_message("See the 'Set up Python Application' -> 'Configure Token' section in the README for more information on the following prompt. In summary, your code will appear in the URL after completing the flow - copy everything after 'code='", "CONFIG", "info")
            print_message("Please visit the following URL and complete the sign in flow: ", "CONFIG", "info")
            print_message(dev_urls["get_auth_code_sub"].format(client_id=user_auth["client_id"]), "CONFIG", "info")
            code = ""
            while not code:
                code = input("Enter code: ")
            dev_config["auth"]["auth_code"] = code
            config_write_dev(dev_config)

        refresh_token = api_get_refresh_token()
        if refresh_token is not None:
            dev_config["auth"]["refresh_token"] = refresh_token
            dev_config["req_bodies"]["refresh_body"] = dev_req_bodies["refresh_body_sub"].format(client_id=user_auth["client_id"], client_secret=user_auth["client_secret"], redirect_uri=dev_urls["redirect_uri"], refresh_token=refresh_token)
            config_write_dev(dev_config)
            print_message("Successfully configured!", "CONFIG", "info")
    else:
        print_message("Your refresh token has already been configured!", "CONFIG", "info")


def main():
    parser = argparse.ArgumentParser()
    setup_parser(parser)

    if parser.parse_args().clear:
        clear_configuration()
    else:
        setup_refresh_token()

if __name__ == '__main__':
    main()
