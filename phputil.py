import json
import os
import re
from urllib.request import urlopen

import constants
import fileutil

verRe = re.compile(r'php-(?P<version>\d+\.\d+\.\d+)-Win', re.IGNORECASE)
zipRe = re.compile(r'(?P<version>php-.*?)\.zip', re.IGNORECASE)


def get_versions():
    """Get the downloaded versions of PHP."""
    subfolders = [
        f.path for f in os.scandir(constants.PHP_DIR) if f.is_dir()
    ]
    versions = {}
    print('PHP versions:')
    for folder in subfolders:
        version = extract_version_string(folder)
        path = folder
        versions[version] = path
        print(version)


def get_releases():
    """Get the released versions of PHP."""
    response = urlopen(constants.PHP_RELEASES_JSON)
    return json.loads(
        response.read()
    )


def extract_version_string(folder: str):
    """Extract the version from the version string."""
    matches = re.search(verRe, folder)
    if matches.group('version'):
        return matches.group('version')
    else:
        return False


def build_download_url(version: str):
    """Build a download URL."""
    return(
        constants.PHP_DOWNLOAD +
        'php-' +
        version +
        '-' +
        constants.PHP_VARIANT +
        '.zip'
    )


def get_version_from_zip(zip_name: str):
    """Extract the version from the zip."""
    matches = re.search(zipRe, zip_name)
    if matches.group('version'):
        return matches.group('version')
    else:
        return False


def download_php(version: str):
    """Download a PHP version"""
    url = build_download_url(version)
    print(f'Getting PHP {version}')
    file_path = fileutil.download_file(url, constants.PHP_DIR)
    if fileutil.unzip_to(file_path, constants.PHP_DIR):
        print(f'PHP {version} downloaded')
        return True
