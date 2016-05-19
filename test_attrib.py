import pytest
import unittest


def test_arg(testdir):
    result = testdir.runpytest("--help")
    result.stdout.fnmatch_lines("*-a ATTREXPR*")

def test_config(testdir):
    config = testdir.parseconfig()
    assert config.getoption('attrexpr') == ''

    config = testdir.parseconfig('-a', 'attr1')
    assert config.getoption('attrexpr') == 'attr1'

    config = testdir.parseconfig('-a', 'attr1==val1 and attr2==True')
    assert config.getoption('attrexpr') == 'attr1==val1 and attr2==True'

    config = testdir.parseconfig('-a', 'attr1==val1 and attr2==True',
                                 '-k', 'somethingelse')
    assert config.getoption('attrexpr') == 'attr1==val1 and attr2==True'

@pytest.mark.parametrize("spec", [
    ("xyz", ("test_one",)),
    ("xyz and xyz2", ()),
    ("xyz2", ("test_two",)),
    ("xyz or xyz2", ("test_one", "test_two"),)
])
def test_functions(spec, testdir):
    testdir.makepyfile("""
        def test_one():
            pass
        test_one.xyz = "xyz"

        def test_two():
            pass
        test_two.xyz2 = "xyz2"
    """)
    opt, passed_result = spec
    rec = testdir.inline_run("-a", opt)
    passed, skipped, fail = rec.listoutcomes()
    passed = [x.nodeid.split("::")[-1] for x in passed]
    assert len(passed) == len(passed_result)
    assert set(passed) == set(passed_result)

@pytest.mark.parametrize("spec", [
    ("xyz", ("test_one",)),
    ("xyz and xyz2", ()),
    ("xyz2", ("test_two",)),
    ("xyz or xyz2", ("test_one", "test_two")),
    ("xyz3", ("test_three",)),
    ("xyz or xyz2 or xyz3", ("test_one", "test_two", "test_three")),
])
def test_classes(spec, testdir):
    testdir.makepyfile("""
        import unittest
        class OneTest(unittest.TestCase):
            def test_one(self):
                pass
        OneTest.xyz = "xyz"

        class TwoTest(unittest.TestCase):
            def test_two(self):
                pass
        TwoTest.xyz2 = "xyz2"

        class ThreeTest(unittest.TestCase):
            def test_three(self):
                pass
            test_three.xyz3 = "xyz3"
    """)
    opt, passed_result = spec
    rec = testdir.inline_run("-a", opt)
    passed, skipped, fail = rec.listoutcomes()
    passed = [x.nodeid.split("::")[-1] for x in passed]
    assert len(passed) == len(passed_result)
    assert set(passed) == set(passed_result)
