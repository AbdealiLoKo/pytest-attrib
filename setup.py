#!/usr/bin/env python

from setuptools import setup
import pytest_attrib


if __name__ == '__main__':
    setup(
        name='pytest-attrib',
        description='pytest plugin to select tests based on attributes '
                    'similar to the nose-attrib plugin',
        long_description=open("README.rst").read(),
        version=pytest_attrib.__version__,
        author='Abdeali JK',
        author_email='abdealikothari@gmail.com',
        url='http://pypi.python.org/pypi/pytest-attrib/',
        py_modules=['pytest_attrib'],
        entry_points={'pytest11': ['attrib = pytest_attrib.plugin']},
        install_requires=['pytest>=2.2'],
        license="MIT License",
        package_data={'file_metadata': ["VERSION"]},
        classifiers=[
            'Development Status :: 4 - Beta',
            'Environment :: Plugins',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: MIT License',
            'Operating System :: POSIX',
            'Operating System :: Microsoft :: Windows',
            'Operating System :: MacOS :: MacOS X',
            'Topic :: Software Development :: Testing',
            'Topic :: Software Development :: Libraries',
            'Topic :: Utilities',
            'Programming Language :: Python',
            'Programming Language :: Python :: 2.6',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3.2',
            'Programming Language :: Python :: 3.3',
            'Programming Language :: Python :: 3.4'])
