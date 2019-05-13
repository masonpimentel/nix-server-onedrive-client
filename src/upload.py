from lib.api import *

from fsplit.filesplit import FileSplit
import tempfile


def maintain_size(token, file_id, pair_index):
    user_limits = config_get_user_limits()
    backup_size = api_get_server_backup_size(token, pair_index)

    while backup_size > user_limits["backup_max_size"]:
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


def get_chunks(tmpdirname, pair_index):
    files = os.listdir(tmpdirname)
    chunks = []
    filename = fs_get_local_filename(pair_index).split(".")[pair_index]
    for file in files:
        if file.startswith(filename):
            chunks.append(file)

    return sorted(chunks)


def main():
    dev_limits = config_get_dev_limits()
    token = api_get_token()

    pair_index = 0
    for dev_upload_path in config_get_dev_paths()["upload_pairs"]:
        file_id = api_get_file_id(token, None, pair_index)
        upload_url = api_create_upload_session(token, pair_index)
        total_size = fs_get_upload_size(pair_index)

        if total_size > dev_limits["upload_partition_limit"]:
            limit = dev_limits["upload_partition_limit"]
            print_message("Greater than " + str(limit / 1024 / 1024) + " MB - need to split into chunks", "UPLOAD", "verbose")

            with tempfile.TemporaryDirectory(dir=fs_get_parent_dir()) as tmpdirname:
                print_message("Created temporary directory: " + tmpdirname, "UPLOAD", "verbose")
                fs = FileSplit(file=dev_upload_path, splitsize=limit, output_dir=tmpdirname)
                fs.split()
                chunks = get_chunks(tmpdirname, pair_index)
                start_byte = 0
                for chunk_name in chunks:
                    chunk_path = fs_get_chunk_full_path(tmpdirname, chunk_name)
                    chunk_size = fs_get_chunk_size(chunk_path)
                    if chunk_size > limit:
                        raise RuntimeError("There was a problem partitioning the tar file")
                    with open(chunk_path, 'rb') as chunk:
                        payload = chunk.read()
                    api_upload_chunk(upload_url, start_byte, start_byte + chunk_size - 1, total_size, payload)
                    start_byte += chunk_size
        else:
            print_message("Uploading entire file in one chunk", "UPLOAD", "verbose")
            with open(dev_upload_path, 'rb') as file:
                payload = file.read()
            api_upload_chunk(upload_url, 0, total_size-1, total_size, payload)

        maintain_size(token, file_id, pair_index)
        pair_index += 1


if __name__ == '__main__':
    main()
