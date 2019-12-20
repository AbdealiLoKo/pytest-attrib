# -*- coding: utf-8 -*-

import pytest


def pytest_addoption(parser):
    group = parser.getgroup("general")
    group._addoption("--eval-attr", "-a", action="store", default="",
                     dest="attrexpr", metavar="ATTREXPR",
                     help='Only run tests matching given attribute expression.'
                          '  Example: -a "attr1==val1 and attr2==val2".')
    group._addoption("--eval-attr-skiperror", action="store_true",
                     dest="skiperrorexpr",
                     help="Treat expression evaluation exception as mismatch.")


def pytest_collection_modifyitems(items, config):
    attrexpr = config.option.attrexpr
    skiperrorexpr = config.option.skiperrorexpr

    if not attrexpr:
        return

    remaining = []
    deselected = []
    for colitem in items:
        if attrexpr and not match_attr(colitem, attrexpr, skiperrorexpr):
            deselected.append(colitem)
        else:
            remaining.append(colitem)

    if deselected:
        config.hook.pytest_deselected(items=deselected)
        items[:] = remaining


def match_attr(item, expr, skip=False):
    # separate `if` to keep `try` Python 2 and 3 compatible
    if not skip:
        return eval(expr, {}, AttrMapping(item))

    try:  # skiperrorexpr == True
        return eval(expr, {}, AttrMapping(item))
    except Exception:
        return False


class AttrMapping:
    """
    Provide a mapping for attributes of an item, where if the attribute does
    not exist, None is given.
    """
    def __init__(self, item):
        self._item = item

    def __getitem__(self, name):
        obj = self._item.obj
        missing_attr = object()

        objattr = getattr(obj, name, missing_attr)
        if objattr != missing_attr:
            return objattr

        cls = self._item.parent
        if isinstance(cls, pytest.Class):
            clsattr = getattr(cls.obj, name, missing_attr)
            if clsattr != missing_attr:
                return clsattr

        return None
