#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
import os
import re


ROOT = os.path.dirname(__file__)
with open(os.path.join(ROOT, 'tears.py')) as fd:
    __version__ = re.search("__version__ = '([^']+)'", fd.read()).group(1)

setup(
    name="tears",
    version=__version__,
    description="SQLAlchemy single connection strategy overwrite to run tests"
                " in a super transaction and rollback at teardown.",
    author="Florian Mounier",
    author_email="florian.mounier@kozea.fr",
    py_modules=["tears"],
    platforms="Any",
    provides=['tears'],
    license="GPLv3",
    install_requires=['sqlalchemy'],
    # tests_require=["pytest"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3"])
