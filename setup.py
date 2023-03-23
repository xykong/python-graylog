#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""setup.py for graylog"""

import codecs
import os
import re
import sys

from setuptools import setup, find_packages
from setuptools.command.test import test


def find_version(*file_paths):
    with codecs.open(
            os.path.join(os.path.abspath(os.path.dirname(__file__)), *file_paths), "r"
    ) as fp:
        version_file = fp.read()
    m = re.search(r"^__version__ = \((\d+), ?(\d+), ?(\d+)\)", version_file, re.M)
    if m:
        return "{}.{}.{}".format(*m.groups())
    raise RuntimeError("Unable to find a valid version")


VERSION = find_version("graylog", "__init__.py")


class Pylint(test):
    def run_tests(self):
        from pylint.lint import Run

        Run(
            [
                "graylog",
                "--persistent",
                "y",
                "--rcfile",
                ".pylintrc",
                "--output-format",
                "colorized",
            ]
        )


class PyTest(test):
    user_options = [("pytest-args=", "a", "Arguments to pass to pytest")]

    def __init__(self, dist, **kw):
        test.__init__(self, dist, **kw)
        self.pytest_args = None

    def initialize_options(self):
        test.initialize_options(self)
        self.pytest_args = "-v --cov={}".format("graylog")

    def run_tests(self):
        import shlex

        # import here, cause outside the eggs aren't loaded
        import pytest

        errno = pytest.main(shlex.split(self.pytest_args))
        sys.exit(errno)


setup(
    name="python-graylog",
    version=VERSION,
    # version=pkg_resources.require("graylog")[0].version,
    description="Python logging handlers that send messages in the Graylog Extended Log Format (GELF).",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    keywords="logging gelf graylog2 graylog udp http",
    author="xy.kong",
    author_email="xy.kong@gmail.com",
    url="https://github.com/xykong/python-graylog",
    license="Apache-2.0",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    tests_require=[
        "pytest>=2.8.7,<4.0.0",
        "pytest-cov<=2.6.0,<3.0.0",
        "pylint>=1.9.3,<2.0.0",
        "mock>=2.0.0,<3.0.0",
        "requests>=2.20.1,<3.0.0",
    ],
    extras_require={
        "docs": [
            "sphinx>=2.1.2,<3.0.0",
            "sphinx_rtd_theme>=0.4.3,<1.0.0",
            "sphinx-autodoc-typehints>=1.6.0,<2.0.0",
        ],
    },
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: System :: Logging",
    ],
    cmdclass={"test": PyTest, "lint": Pylint},
)
