import pytest


def test_arg(testdir):
    result = testdir.runpytest("--help")
    result.stdout.fnmatch_lines("*--attr=ATTR*")
