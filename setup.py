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
with open('README.rst') as f:
    readme = f.read()


setup(
    name='convertbng',
    version=version,
    description='Fast lon, lat to and from ETRS89 and BNG (OSGB36) using Rust FFI',
    author='Stephan Hügel',
    author_email='urschrei@gmail.com',
    license='MIT License',
    url='https://github.com/urschrei/convertbng',
    include_package_data=True,
    distclass=BinaryDistribution,
    download_url='https://github.com/urschrei/convertbng/tarball/v%s' % version,
    keywords=['Geo', 'BNG', 'OSGB36', 'GIS', 'ETRS89', 'OSTN02'],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Education',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Scientific/Engineering :: GIS',
    ],
    packages=find_packages(),
    install_requires=['numpy >= 1.9.0'],
    long_description=readme
)
