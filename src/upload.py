from fs import *
from api import *

from fsplit.filesplit import FileSplit


def maintain_size(token, file_id):
    limits = config_get_limits()
    backup_size = api_get_server_backup_size(token)

    while backup_size > limits["backup_max_size"]:
        print_message("Current backup size: " + "{:.0f}".format(backup_size / 1024 / 1024) + " MB", "UPLOAD", "verbose")
        delete_oldest(token, file_id)
        backup_size = api_get_server_backup_size(token)


def delete_oldest(token, file_id):
    files = api_get_all_backups(token, file_id)
    files.sort()
    oldest = files[0]
    file_id = api_get_file_id(token, oldest)
    print_message("Deleting " + file_id, "UPLOAD", "verbose")
    api_delete_file(token, file_id)


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
        "upload_url": api_create_upload_session(token),
        "total_size": fs_get_upload_size()
    }

    return upload_dict

def main():
    # TODO: check server backup size is correct before continuing

    limits = config_get_limits()
    paths = config_get_paths()

    upload_dict = create_upload_dict()
    if not upload_dict:
        return

    total_size = upload_dict["total_size"]
    if total_size > limits["upload_partition_limit"]:
        limit = limits["upload_partition_limit"]
        limit_mb = str(limit / 1024 / 1024)
        upload_url = upload_dict["upload_url"]
        local_dir = paths["upload_pairs"][0]["local_dir"]
        print_message("Greater than " + limit_mb + "MB - need to split into chunks", "UPLOAD", "verbose")

        # TODO: make this iterate through all the paths
        fs = FileSplit(file=local_dir, splitsize=limit)
        # TODO this should be done in a tmp directory and garbage collected
        fs.split()
        chunks = get_chunks()
        start_byte = 0
        for chunk_name in chunks:
            chunk_size = fs_get_chunk_size(chunk_name)
            if chunk_size > limit:
                print_message("There was a problem partitioning the tar file", "UPLOAD", "error")
                return
            with open(chunk_name, 'rb') as chunk:
                payload = chunk.read()
            api_upload_chunk(upload_url, start_byte, start_byte + chunk_size - 1, total_size, payload)
            start_byte += chunk_size
    else:
        print_message("Uploading entire file in one chunk", "UPLOAD", "verbose")
        with open(paths["upload_pairs"][0]["local_dir"], 'rb') as file:
            payload = file.read()
        if not api_upload_chunk(upload_dict["upload_url"], 0, total_size-1, total_size, payload):
            return

    # need to keep within 50 GB
    #maintain_size(token, file_id)


if __name__ == '__main__':
    main()
