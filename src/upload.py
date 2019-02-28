import os

from fs import *
from api import *

from fsplit.filesplit import FileSplit

# with open("../config.json") as e_config_file:
#     e_json_config = json.load(e_config_file)
#     BACKUP_MAX_SIZE = e_json_config["limits"]["backup_max_size"]
#     UPLOAD_PARTITION_LIMIT = e_json_config["limits"]["upload_partition_limit"]
#     UPLOAD_PATHS = e_json_config["paths"]["upload"]


def delete_oldest(token, file_id):
    files = api_get_all_backups(token, file_id)
    files.sort()
    oldest = files[0]
    file_id = api_get_file_id(token, oldest)
    print("Deleting " + file_id)
    api_delete_file(token, file_id)


def maintain_size(token, file_id):
    backup_size = api_get_server_backup_size(token)
    while backup_size > BACKUP_MAX_SIZE:
        print("Current backup size: " + str(backup_size / 1024 / 1024) + "MB")
        delete_oldest(token, file_id)
        backup_size = api_get_server_backup_size(token)
    else:
        return


def get_chunks():
    files = os.listdir(".")
    chunks = []
    filename = fs_get_local_filename().split(".")[0]
    for file in files:
        if file.startswith(filename):
            chunks.append(file)
    return chunks


def create_upload_dict():
    token = api_get_token()

    upload_dict = {
        "token": token,
        "file_id": api_get_file_id(token, None),
        "upload_url": api_create_upload_session(token)
    }

    for key in upload_dict.keys():
        if not upload_dict[key]:
            return None

    return upload_dict

def main():
    upload_dict = create_upload_dict()
    if not upload_dict:
        return

    total_size = fs_get_upload_size()
    if total_size > UPLOAD_PARTITION_LIMIT:
        print("Greater than 60 MB - need to split into chunk_name")
        # TODO: make this iterate through all the paths
        fs = FileSplit(file=UPLOAD_PATHS[0], splitsize=UPLOAD_PARTITION_LIMIT)
        fs.split()
        chunks = get_chunks()
        start_byte = 0
        for chunk_name in chunks:
            chunk_size = fs_get_chunk_size(chunk_name)
            if chunk_size > UPLOAD_PARTITION_LIMIT:
                print("Chunk too big")
                # TODO: throw error
            with open(chunk_name, 'rb') as chunk:
                payload = chunk.read()
            api_upload_chunk(upload_url, start_byte, start_byte + chunk_size - 1, total_size, payload)
            start_byte += chunk_size
    else:
        print("Uploading entire file in one chunk")
        with open(UPLOAD_PATHS[0], 'rb') as file:
            payload = file.read()
        api_upload_chunk(upload_url, 0, total_size-1, total_size, payload)

    # need to keep within 50 GB
    maintain_size(token, file_id)


if __name__ == '__main__':
    main()
