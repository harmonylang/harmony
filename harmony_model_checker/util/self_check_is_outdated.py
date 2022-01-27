import json
import atexit
import logging
import time
import pkg_resources
import tempfile
import pathlib

import requests

from harmony_model_checker.util import logger

_logger = logger.get_logger(__name__)


def _get_latest_version(package: str):
    try:
        resp = requests.get(
            f'https://pypi.python.org/pypi/{package}/json', timeout=2)
        if resp.status_code == 200:
            data = resp.json()
            return data['info']['version']
        return '???'
    except requests.exceptions.Timeout:
        return '???'


def _cache_is_valid(expiration: int):
    return time.time() < expiration


def _get_cache_file(package: str):
    return pathlib.Path(tempfile.gettempdir()) / f"{package}_version_cache"


def _log_messages(messages: list):
    for args in messages:
        _logger.log(*args)


def check_outdated(package: str, version: str) -> None:
    """[check_outdated] checks if the version of a package is the
    latest version by calling the PyPi registry. To avoid excessive
    online checks, the latest version string is cached as a file. The
    cache is used for a day.

    Args:
        package (str): [name of the package]
        version (str): [current version to compare against]
    """
    messages_to_log = []
    try:
        parsed_version = pkg_resources.parse_version(version)
        latest = None

        cache_file = _get_cache_file(package)

        if cache_file.exists():
            content = cache_file.read_text()
            latest, last_cached = json.loads(content)
            if not _cache_is_valid(last_cached):
                latest = None

        if latest is None:
            latest = _get_latest_version(package)
        parsed_latest = pkg_resources.parse_version(latest)

        if parsed_version > parsed_latest:
            latest = _get_latest_version(package)
            parsed_latest = pkg_resources.parse_version(latest)

            if parsed_version > parsed_latest:
                # no message to avoid issues in development
                return

        is_latest = parsed_version == parsed_latest
        if not is_latest:
            messages_to_log.append([
                logging.WARNING,
                "Version %s of %s is currently installed, but a new version %s is available.\n"
                "You should consider upgrading to the newer version by running the following command:\n"
                "pip install --upgrade %s",
                version, package, latest, package
            ])
            return
        cache_file.write_text(
            json.dumps([
                latest,
                time.time() + 86400  # number of seconds in a day
            ]))
    except Exception:
        messages_to_log.append([
            logging.ERROR,
            'Error occurred while checking if the current version of Harmony is the latest.'
        ])
    finally:
        atexit.register(_log_messages, messages_to_log)
