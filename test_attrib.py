import pytest


def check_passed(spec, testdir, with_parent=False):
    opt = spec[0]
    expected_results = spec[1:]  # passed, skipped, failed

    rec = testdir.inline_run("-a", opt)
    actual_results = rec.listoutcomes()
    actual_results = actual_results[:len(expected_results)]

    for expected, actual in zip(expected_results, actual_results):
        if with_parent:
            actual = ["::".join(x.nodeid.split("::")[-2:]) for x in actual]
        else:
            actual = [x.nodeid.split("::")[-1] for x in actual]
        assert len(actual) == len(expected)
        assert set(actual) == set(expected)


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
        def test_one(): pass
        test_one.xyz = "xyz"

        def test_two(): pass
        test_two.xyz2 = "xyz2"
    """)
    return check_passed(spec, testdir)


@pytest.mark.parametrize("spec", [
    ("xyz", (), ("test_one",)),
    ("xyz2", ("test_two",)),
    ("1", ("test_two",), ("test_one",)),  # Test without -a
])
def test_functions_decorated(spec, testdir):
    testdir.makepyfile("""
        import unittest

        @unittest.skipIf(1 == 1, 'From test_one')
        def test_one(): pass
        test_one.xyz = "xyz"

        @unittest.skipIf(1 == 0, 'From test_two')
        def test_two(): pass
        test_two.xyz2 = "xyz2"
    """)
    return check_passed(spec, testdir)


@pytest.mark.parametrize("spec", [
    ("xyz", ("OneTest::test_one", "TwoTest::test_one", "TwoTest::test_two")),
    ("xyz2", ("TwoTest::test_one", "TwoTest::test_two",)),
    ("xyz3", ("ThreeTest::test_three",)),
    ("xyz2 or xyz3", ("TwoTest::test_one", "TwoTest::test_two",
                      "ThreeTest::test_three")),
])
def test_classes(spec, testdir):
    testdir.makepyfile("""
        import unittest
        class OneTest(unittest.TestCase):
            def test_one(self): pass
        OneTest.xyz = "xyz"

        class TwoTest(OneTest):  # Inherited
            def test_two(self): pass
            xyz2 = "xyz2"

        class ThreeTest(unittest.TestCase):
            def test_three(self): pass
            test_three.xyz3 = "xyz3"
    """)
    return check_passed(spec, testdir, with_parent=True)


@pytest.mark.parametrize("spec", [
    ("xyz=='xyz'", ("test_one",)),
    ("xyz=='xyz2'", ()),
    ("xyz=='xyz2' or xyz2", ("test_two",)),
    ("xyz=='xyz2' and xyz2=='xyz'", ()),
    ("xyz=='xyz' and xyz2=='xyz2'", ()),
])
def test_conditionals(spec, testdir):
    testdir.makepyfile("""
        import unittest
        class OneTest(unittest.TestCase):
            def test_one(self): pass
            xyz = "xyz"

        class TwoTest(unittest.TestCase):
            def test_two(self): pass
            xyz2 = "xyz2"
    """)
    return check_passed(spec, testdir)
