#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
'''
Description:
        setup.py that install necessary python mods, pychat_server.py and chatter_box.py

Author:
        Daniel Gregory (gigs94@gmail.com)

Licence:
        The MIT License (MIT)

        Copyright (c) 2015 Daniel Gregory

        Permission is hereby granted, free of charge, to any person obtaining a copy
        of this software and associated documentation files (the "Software"), to deal
        in the Software without restriction, including without limitation the rights
        to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
        copies of the Software, and to permit persons to whom the Software is
        furnished to do so, subject to the following conditions:

        The above copyright notice and this permission notice shall be included in
        all copies or substantial portions of the Software.

        THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
        IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
        FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
        AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
        LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
        OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
        THE SOFTWARE.
'''

import sys
try:
    from setuptools import setup
    has_setuptools = True
except ImportError:
    from distutils.core import setup
    has_setuptools = False



requirements = ['python-gnupg', 'argparse', 'pika', 'ConfigParser' ]


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
    scripts = ['src/chatter_box.py','src/pychat_server.py'],
    **setuptools_options
)
