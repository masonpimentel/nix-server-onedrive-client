from api import *
import json


def write_to_dev_config(new_config, msg):
    with open("../dev_config.json", "w") as config_file:
        json.dump(new_config, config_file, indent=4, sort_keys=True)
    print_message(msg, "CONFIG", "info")


def main():
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
            # TODO add section
            print_message("See guide TODO for more information on the following prompt. The code will appear in the URL after completing the flow, copy everything after 'code='", "CONFIG", "info")
            print_message("Please visit the following URL and complete the sign in flow: " + dev_urls["get_auth_code_sub"].format(client_id=user_auth["client_id"]), "CONFIG", "info")
            print_message("A prompt will appear below where you can enter your code.", "CONFIG", "info")
            code = ""
            while not code:
                code = input("Enter code: ")
            dev_config["auth"]["auth_code"] = code
            write_to_dev_config(dev_config, "Successfully added auth code!")

        refresh_token = api_get_refresh_token()
        if refresh_token is not None:
            dev_config["auth"]["refresh_token"] = refresh_token
            dev_config["req_bodies"]["refresh_body"] = dev_req_bodies["refresh_body_sub"].format(client_id=user_auth["client_id"], client_secret=user_auth["client_secret"], redirect_uri=dev_urls["redirect_uri"], refresh_token=refresh_token)
            write_to_dev_config(dev_config, "Successfully configured!")
    else:
        print_message("Your refresh token has already been configured!", "CONFIG", "info")


if __name__ == '__main__':
    main()
