import requests
import json
from fs import *
from debugging import *
from utils import *

#TODO need to handle incorrect refresh token

def api_create_urlencoded_header():
    return {
        'Content-Type': 'application/x-www-form-urlencoded'
    }


def api_create_get_header(token):
    return {
        'Authorization': token,
        'Content-Type': 'application/json'
    }


def api_get_refresh_token():
    urls = config_get_urls()
    auth = config_get_auth()
    req_bodies = config_get_req_bodies()

    h = api_create_urlencoded_header()
    b = req_bodies["api_get_refresh_token_sub"]
    b = b.format(client_id=auth["client_id"], client_secret=auth["client_secret"], redirect_uri=urls["redirect_uri"], auth_code=auth["auth_code"])
    r = requests.post(urls["api_get_refresh_token"], data=b, headers=h)
    r_parsed = r.json()
    if "error" in r_parsed.keys():
        if r_parsed["error"] == "invalid_grant":
            # TODO add section
            print_message("Your auth code has expired. Please refer to TODO to get a new one.", "CONFIG", "error")
        elif r_parsed["error"] == "invalid_client":
            print_message("Something went wrong with the client auth info you entered - either the client ID or client secret is incorrect. Please refer to the steps in TODO.", "CONFIG", "error")
        else:
            print_message("Unexpected error getting refresh token", "CONFIG", "error")
            if "error_description" in r_parsed.keys():
                print_message("Error description: " + r_parsed["error_description"], "CONFIG", "error")
        return None
    else:
        return r.json()["refresh_token"]


def api_get_file_id(token, filename):
    if filename is None:
        url = URL_ROOT + "/me/drive/root:/ServerBackup"
    else:
        url = URL_ROOT + "/me/drive/root:/ServerBackup/" + filename
    r = requests.get(url, headers=api_create_get_header(token))
    return r.json()["id"]


def api_get_token():
    h = api_create_urlencoded_header()
    r = requests.post("https://login.live.com/oauth20_token.srf", data=config_get_req_bodies()["refresh_body"], headers=h)
    r_parsed = r.json()
    if "access_token" not in r_parsed.keys():
        return None
    return r.json()["access_token"]


def api_delete_file(token, file_id):
    url = URL_ROOT + "/me/drive/items/" + file_id
    requests.delete(url, headers=api_create_get_header(token))
    # TODO check for 204 - and make some kind of max attempts check
    return


def api_create_upload_session(token):
    url = URL_ROOT + "/drive/root:/ServerBackup/" + fs_get_filename() + ":/createUploadSession"
    r = requests.post(url, headers=api_create_get_header(token))
    return r.json()["uploadUrl"]


def api_upload_chunk(url, bottom, top, total, payload):
    length = top - bottom + 1
    c_range = "bytes " + str(bottom) + "-" + str(top) + "/" + str(total)
    h = {
        'Content-Length': str(length),
        'Content-Range': c_range
    }
    print("Uploading " + str(h))
    r = requests.put(url, data=payload, headers=h)
    print("Status: " + str(r.status_code))


def api_get_server_backup_size(token):
    url = URL_ROOT + "/me/drive/root:/ServerBackup"
    r = requests.get(url, headers=api_create_get_header(token))
    return r.json()["size"]


def api_get_all_backups(token, file_id):
    url = URL_ROOT + "/me/drive/items/" + file_id + "/children"
    r = requests.get(url, headers=api_create_get_header(token))
    children = r.json()["value"]
    filenames = []
    for child in children:
        filenames.append(child["name"])
    return filenames
