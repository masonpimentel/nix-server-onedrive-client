from api import *

from fsplit.filesplit import FileSplit
import tempfile


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


def get_chunks(tmpdirname):
    files = os.listdir(tmpdirname)
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

    total_size = upload_dict["total_size"]
    # TODO: make this iterate through all the paths
    if total_size > limits["upload_partition_limit"]:
        limit = limits["upload_partition_limit"]
        print_message("Greater than " + str(limit / 1024 / 1024) + "MB - need to split into chunks", "UPLOAD", "verbose")

        with tempfile.TemporaryDirectory(dir=fs_get_parent_dir()) as tmpdirname:
            print_message("Created temporary directory: " + tmpdirname, "UPLOAD", "verbose")
            fs = FileSplit(file=paths["upload_pairs"][0]["local_tar"], splitsize=limit, output_dir=tmpdirname)
            fs.split()
            chunks = get_chunks(tmpdirname)
            start_byte = 0
            for chunk_name in chunks:
                chunk_path = fs_get_chunk_full_path(tmpdirname, chunk_name)
                chunk_size = fs_get_chunk_size(chunk_path)
                if chunk_size > limit:
                    raise RuntimeError("There was a problem partitioning the tar file")
                with open(chunk_path, 'rb') as chunk:
                    payload = chunk.read()
                api_upload_chunk(upload_dict["upload_url"], start_byte, start_byte + chunk_size - 1, total_size, payload)
                start_byte += chunk_size
    else:
        print_message("Uploading entire file in one chunk", "UPLOAD", "verbose")
        with open(paths["upload_pairs"][0]["local_tar"], 'rb') as file:
            payload = file.read()
        if not api_upload_chunk(upload_dict["upload_url"], 0, total_size-1, total_size, payload):
            return

    # need to keep within 50 GB
    maintain_size(upload_dict["token"], upload_dict["file_id"])


if __name__ == '__main__':
    main()
