# -*- coding: utf-8 -*-

import pytest

__version__ = '0.1'


def pytest_addoption(parser):
    group = parser.getgroup("general")
    group._addoption("-a", action="store", default="",
                     dest="attrexpr", metavar="ATTREXPR",
                     help='Only run tests matching given attribute expression.'
                          '  Example: -a "attr1==val1 and attr2==val2".')


def pytest_collection_modifyitems(items, config):
    attrexpr = config.option.attrexpr

    if not attrexpr:
        return

    remaining = []
    deselected = []
    for colitem in items:
        if attrexpr and not match_attr(colitem, attrexpr):
            deselected.append(colitem)
        else:
            remaining.append(colitem)

    if deselected:
        config.hook.pytest_deselected(items=deselected)
        items[:] = remaining


def match_attr(item, expr):
    return eval(expr, {}, AttrMapping(item))


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
