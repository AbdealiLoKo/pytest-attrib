.. image:: https://travis-ci.org/AbdealiJK/pytest-attrib.svg?branch=master
    :target: https://travis-ci.org/AbdealiJK/pytest-attrib

.. image:: https://ci.appveyor.com/api/projects/status/1q5qdliai6hu4hrv/branch/master?svg=true
    :target: https://ci.appveyor.com/project/AbdealiJK/pytest-attrib

pytest-attrib
=============

The `pytest-attrib`_ plugin extends py.test with the ability to select tests
based on a criteria rather than just the filename or pytest.marks. For
example, you might want to run only tests that need internet connectivity,
or tests that are slow.

The `pytest.mark <https://pytest.org/latest/mark.html>`__ plugin already
provides a featrure to mark tests and run only the marked tests. This plugin
also allows to run expressions on the attributes of the class, and does not
require the pytest.mark decorator.

It offers features similar to the nose plugin
`nose-attrib <http://nose.readthedocs.io/en/latest/plugins/attrib.html>`__.

Installation
------------

Install the plugin with::

    pip install pytest-attrib

Usage examples
--------------

To use the plugin, the ``-a`` CLI argument has been provided. Consider a
project with the test file::

    import unittest

    class MyTestCase(unittest.TestCase):
        def test_function(self):
            assert 1 == 1

    class MySlowTestCase(unittest.TestCase):
        slow = True

        def test_slow_function(self):
            import time
            time.sleep(5)
            assert 1 == 1

Using pytest-attrib, only the slow tests can be run using::

    $ py.test -a slow

Or run only the fast tests using::

    $ py.test -a "not slow"

The expression given in the ``-a`` argument can be even more complex, for
example::

    $ py.test -a "slow and requires_internet"
    $ py.test -a "slow and not requires_internet"

It can also do conditional arguments like::

    $ py.test -a "speed=='slow' and requires_internet"

LICENSE
-------

.. image:: https://img.shields.io/github/license/AbdealiJK/pytest-attrib.svg
   :target: https://opensource.org/licenses/MIT

This code falls under the
`MIT License <https://tldrlegal.com/license/mit-license>`__.
Please note that some files or content may be copied from other places
and have their own licenses. Dependencies that are being used to generate
the databases also have their own licenses.
