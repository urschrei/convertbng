#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
setup.py

Created by Stephan Hügel on 2015-06-21
"""
from __future__ import unicode_literals
import os
import re
import io
from setuptools import setup, find_packages, Distribution

def read(*names, **kwargs):
    with io.open(
        os.path.join(os.path.dirname(__file__), *names),
        encoding=kwargs.get("encoding", "utf8")
    ) as fp:
        return fp.read()

def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(
        r"^__version__ = ['\"]([^'\"]*)['\"]",
        version_file,
        re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

class BinaryDistribution(Distribution):
    def is_pure(self):
        return False

version=find_version("convertbng/util.py")

setup(
    name='convertbng',
    version=version,
    description='Fast lon, lat to BNG conversion',
    author='Stephan Hügel',
    author_email='urschrei@gmail.com',
    license='MIT License',
    url='https://github.com/urschrei/rust_bng',
    include_package_data=True,
    distclass=BinaryDistribution,
    download_url='https://github.com/urschrei/rust_bng/tarball/v%s' % version,
    keywords=['Geo'],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    packages=find_packages(),
    long_description="""\
Fast lon, lat to BNG conversion
---------------------------------------------

Uses a Rust 1.0 binary to perform fast lon, lat to BNG conversion\n
This module exposes a single method: util.convertbng()\n
call it like so:\n\n
from convertbng.util import convertbng\n
res = convertbng(lon, lat)\n\n

This version requires Python 2.7.x / 3.4.x"""
)
