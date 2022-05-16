import argparse

import constants
import phputil

parser = argparse.ArgumentParser()
parser.add_argument(
    '--download',
    dest='download_version',
    action='store',
    type=str,
    metavar='version',
    help='download PHP version (e.g. 7.2.0)'
)
parser.add_argument(
    '--list',
    action='store_true',
    help='list PHP versions'
)
parser.add_argument(
    '--config',
    action='store_true',
    help='show config'
)


def list_config():
    """List the configuration."""
    for constant in constants.__dict__:
        if constant.startswith('PHP'):
            print(f"{constant} = {constants.__dict__[constant]}")


if __name__ == '__main__':
    args = parser.parse_args()
    if args.list:
        phputil.get_versions()
    elif args.config:
        list_config()
    elif args.download_version:
        phputil.download_php(args.download_version)
    else:
        phputil.get_versions()
