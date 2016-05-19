import pytest

pytest_plugins = "pytester"

@pytest.fixture
def testdir(testdir):
    # pytest before 2.8 did not have a runpytest_subprocess
    if not hasattr(testdir, "runpytest_subprocess"):
        testdir.runpytest_subprocess = testdir.runpytest
    return testdir
