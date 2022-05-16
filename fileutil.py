import os
import shutil

import requests
from clint.textui import progress

import constants
import phputil

chunk_size = 1024 * 8


def check_config():
    """Check the configuration."""
    if not os.path.exists(constants.PHP_DIR):
        return False
    else:
        return True


def download_file(url: str, dest_folder: str):
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)

    filename = url.split('/')[-1].replace(" ", "_")
    file_path = os.path.join(dest_folder, filename)

    r = requests.get(url, stream=True)
    if r.ok:
        with open(file_path, 'wb') as f:
            total_length = int(
                r.headers.get('content-length')
            )
            expected_size = (total_length/chunk_size) + 1
            for chunk in progress.bar(
                r.iter_content(chunk_size=chunk_size),
                expected_size=expected_size
            ):
                if chunk:
                    f.write(chunk)
                    f.flush()
                    os.fsync(f.fileno())
        return os.path.abspath(file_path)
    else:  # HTTP status code 4XX/5XX
        print("Download failed: status code {}\n{}".format(
            r.status_code, r.text
        ))
        return False


def unzip_to(zip_file: str, dest_folder: str):
    if os.path.exists(zip_file):
        dest_folder = os.path.join(
            dest_folder,
            phputil.get_version_from_zip(
                zip_file
            )
        )
        if not os.path.exists(dest_folder):
            shutil.unpack_archive(zip_file, dest_folder)
            clean_up(zip_file)
            return True
        else:
            print("Destination folder already exists, stopping")
            clean_up(zip_file)
            return False
    else:
        print("Downloaded zip not found")
        return False


def clean_up(file: str):
    if os.path.exists(file):
        os.remove(file)
