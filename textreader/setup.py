#!/usr/bin/env python

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


readme = open('README.rst').read()
doclink = """
Documentation
-------------

The full documentation is at http://textreader.rtfd.org."""
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='textreader',
    version='0.0.3',
    description='AWS Lambda with Python 3.6',
    long_description=readme + '\n\n' + doclink + '\n\n' + history,
    author='Timo Koola',
    author_email='timo@skadi.chat',
    url='https://github.com/timokoola/textreader',
    packages=[
        'textreader',
    ],
    package_dir={'textreader': 'textreader'},
    include_package_data=True,
    install_requires=[
    ],
    license='MIT',
    zip_safe=False,
    keywords='textreader',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
)
