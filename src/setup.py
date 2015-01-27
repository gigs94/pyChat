#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2007-2009 Christopher Lenz
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution.

import sys
try:
    from setuptools import setup
    has_setuptools = True
except ImportError:
    from distutils.core import setup
    has_setuptools = False



requirements = ['python-gnupg', 'couchdb', 'Tkinter', 'argparse', 'logging', 'json', 'pika', 'ConfigParser', 'pika' ]


# Build setuptools-specific options (if installed).
if not has_setuptools:
    print("WARNING: setuptools/distribute not available. Please install %s packages manually" % (requirements))
    setuptools_options = {}
else:
    setuptools_options = {
        'install_requires': requirements,
        'test_suite': 'pyChat.tests.__main__.suite',
        'zip_safe': True,
    }


setup(
    name = 'pyChat',
    version = '0.1',
    description = 'Python Chat Client/Server',
    long_description = \
"""This is a pyChat server installation. It provides a simple chat client/server
with gnupg encrypted messages.""",
    author = 'daniel gregory',
    author_email = 'gigs94@gmail.com',
    maintainer = 'daniel gregory',
    maintainer_email = 'gigs94@gmail.com',
    license = 'MIT',
    url = 'https://github.com/gigs94/pyChat',
    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Database :: Front-Ends',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    packages = ['pyChat'],
    **setuptools_options
)
