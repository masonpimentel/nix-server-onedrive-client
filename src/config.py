from api import *
import json


def write_to_config(new_config, msg):
    with open("../config.json", "w") as config_file:
        json.dump(new_config, config_file, indent=4, sort_keys=True)
    print_message(msg, "CONFIG", "info")


def main():
    json_config = config_get_root()
    auth = config_get_auth()
    urls = config_get_urls()
    req_bodies = config_get_req_bodies()

    if not req_bodies["refresh_body"]:
        if auth["client_id"] == "fill_me_in" or auth["client_secret"] == "fill_me_in":
            # TODO add section
            print_message("Client auth info not added to config. Please refer to TODO", "CONFIG", "error")
            return
        if not auth["auth_code"]:
            # TODO add section
            print_message("See guide TODO for more information on the following prompt. The code will appear in the URL after completing the flow, copy everything after 'code='", "CONFIG", "info")
            print_message("Please visit the following URL and complete the sign in flow: " + urls["get_auth_code_sub"].format(client_id=auth["client_id"]), "CONFIG", "info")
            print_message("A prompt will appear below where you can enter your code.", "CONFIG", "info")
            code = ""
            while not code:
                code = input("Enter code: ")
            json_config["auth"]["auth_code"] = code
            write_to_config(json_config, "Successfully added auth code!")

        refresh_token = api_get_refresh_token()
        if refresh_token is not None:
            json_config["auth"]["refresh_token"] = refresh_token
            json_config["req_bodies"]["refresh_body"] = req_bodies["refresh_body_sub"].format(client_id=auth["client_id"], client_secret=auth["client_secret"], redirect_uri=urls["redirect_uri"], refresh_token=refresh_token)
            write_to_config(json_config, "Successfully configured!")
    else:
        print_message("Your refresh token has already been configured!", "CONFIG", "info")


if __name__ == '__main__':
    main()
