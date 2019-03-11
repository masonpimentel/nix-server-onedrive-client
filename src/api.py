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


def check_200_status(code):
    return 200 <= code < 300


def api_upload_error_parser(response, generic_msg):
    print_message(generic_msg, "UPLOAD", "error")
    # TODO error handle incorrectly configured local or server dir
    if "error_description" in response.keys():
        print_message("Error description: " + response["error_description"], "UPLOAD", "error")


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


def api_get_token():
    urls = config_get_urls()

    h = api_create_urlencoded_header()
    r = requests.post(urls["api_get_refresh_token"], data=config_get_req_bodies()["refresh_body"], headers=h)
    r_parsed = r.json()
    if "access_token" not in r_parsed.keys():
        api_upload_error_parser(r_parsed, "Unexpected error getting token")
        return None
    else:
        return r.json()["access_token"]


def api_get_file_id(token, filename):
    urls = config_get_urls()
    upload_pairs = config_get_paths()["upload_pairs"]

    if filename is None:
        url = urls["url_root"] + urls["directory_sub"].format(directory=upload_pairs[0]["server_dir"])
    else:
        url = urls["url_root"] + urls["directory_filename_sub"].format(directory=upload_pairs[0]["server_dir"], filename=filename)
    r = requests.get(url, headers=api_create_get_header(token))
    r_parsed = r.json()
    if "id" not in r_parsed.keys():
        raise RuntimeError("Unexpected error creating upload session")
    else:
        return r.json()["id"]


def api_create_upload_session(token):
    urls = config_get_urls()

    server_filename = fs_get_filename(config_get_paths()["upload_pairs"][0]["server_dir"])
    url = urls["url_root"] + urls["directory_sub"].format(directory=server_filename) + "/" + fs_get_local_filename() + ":/createUploadSession"
    r = requests.post(url, headers=api_create_get_header(token))
    r_parsed = r.json()
    if "uploadUrl" not in r_parsed.keys():
        raise RuntimeError("Unexpected error creating upload session")
    else:
        return r.json()["uploadUrl"]


def api_upload_chunk(url, bottom, top, total, payload):
    length = top - bottom + 1
    c_range = "bytes " + str(bottom) + "-" + str(top) + "/" + str(total)
    h = {
        'Content-Length': str(length),
        'Content-Range': c_range
    }
    print_message("Uploading " + str(h), "UPLOAD", "verbose")
    r = requests.put(url, data=payload, headers=h)
    if not check_200_status(r.status_code):
        raise RuntimeError("Error uploading chunk, status: " + str(r.status_code))


def api_get_server_backup_size(token):
    urls = config_get_urls()
    upload_pairs = config_get_paths()["upload_pairs"]

    url = urls["url_root"] + urls["directory_sub"].format(directory=upload_pairs[0]["server_dir"])
    r = requests.get(url, headers=api_create_get_header(token))
    r_parsed = r.json()
    if "size" not in r_parsed.keys():
        raise RuntimeError("Unexpected error getting server directory size")
    else:
        return r.json()["size"]


def api_get_all_backups(token, file_id):
    urls = config_get_urls()

    url = urls["url_root"] + urls["directory_children_sub"].format(file_id=file_id)
    r = requests.get(url, headers=api_create_get_header(token))
    r_parsed = r.json()

    if "value" not in r_parsed.keys():
        raise RuntimeError("Unexpected error getting server backups")
    else:
        children = r.json()["value"]

    filenames = []
    for child in children:
        filenames.append(child["name"])
    return filenames


def api_delete_file(token, file_id):
    urls = config_get_urls()

    url = urls["url_root"] + urls["file_id_sub"].format(file_id=file_id)
    r = requests.delete(url, headers=api_create_get_header(token))
    if not check_200_status(r.status_code):
        raise RuntimeError("Error clearing file to restore backup size, exiting. Status: " + str(r.status_code))
