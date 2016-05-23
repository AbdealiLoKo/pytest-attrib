import os

VERSION_FILE = os.path.join(os.path.dirname(__file__), "VERSION")


def get_version():
    with open(VERSION_FILE, 'r') as ver:
        return ver.readline().strip()

__version__ = get_version()
