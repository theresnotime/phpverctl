"""Keys, URLs, and other constants."""
import os
import typing

import dotenv

dotenv.load_dotenv()

PHP_DIR = typing.cast(
    str,
    os.path.abspath(
        os.getenv('PHP_DIR')
    )
)  # type: ignore

PHP_DOWNLOAD = typing.cast(str, os.getenv('PHP_DOWNLOAD'))  # type: ignore
PHP_VARIANT = typing.cast(str, os.getenv('PHP_VARIANT'))  # type: ignore

PHP_RELEASES_JSON = typing.cast(
    str,
    PHP_DOWNLOAD + 'releases.json'
)  # type: ignore
