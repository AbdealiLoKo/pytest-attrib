# -*- coding: utf-8 -*-

__version__ = '0.1'


def pytest_addoption(parser):
    group = parser.getgroup("general")
    group._addoption("--attr", dest="attr", action="append", metavar="ATTR",
                     help="Run only tests that have the attributes ATTR")
