# -*- coding: utf-8 -*-

import inspect
import sys

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


def get_class_that_defined_method(meth):
    # In python3 there is no concept of unbound methods and a class
    # method is simply a function.
    # This is a function that attempts to find the class of the method.
    # Taken from:
    # http://stackoverflow.com/questions/3589311/get-defining-class-of-unbound-method-object-in-python-3
    if sys.version_info[0] == 2:
        return getattr(meth, 'im_class', None)
    else:
        if inspect.ismethod(meth):
            for cls in inspect.getmro(meth.__self__.__class__):
                if cls.__dict__.get(meth.__name__) is meth:
                    return cls
            meth = meth.__func__  # fallback to __qualname__ parsing
        if inspect.isfunction(meth):
            cls = getattr(
                inspect.getmodule(meth),
                meth.__qualname__.split('.<locals>', 1)[0].rsplit('.', 1)[0])
            if isinstance(cls, type):
                return cls
    return None  # Failed to find class


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

        cls = get_class_that_defined_method(obj)
        if cls is not None:
            clsattr = getattr(cls, name, missing_attr)
            if clsattr != missing_attr:
                return clsattr

        return None
