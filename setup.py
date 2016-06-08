#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
setup.py

Created by Stephan Hügel on 2015-06-21
"""
# from __future__ import unicode_literals
import os
import sys
import re
import io
import requests
import cStringIO
import zipfile
import tarfile
from setuptools import setup, find_packages, Distribution, Extension
# from Cython.Build import cythonize

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

try:
    from Cython.Build import cythonize
    has_cython = True
except ImportError:
    has_cython = False

# If Cython is installed, use it. Otherwise, build from source
if has_cython:
    suffix = '.pyx'
else:
    suffix = '.c'

# We need to build the module using a Rust binary
# This logic tries to grab it from GitHub, based on the platform

# Get latest Binary from Github
# get GH access token from Travis
ghkey = os.environ['LATEST_TAG']
project = 'lonlat_bng'
latest_release = requests.get(
    "https://api.github.com/repos/urschrei/%s/releases/latest" % project,
    headers={'Authorization':'access_token %s' % ghkey}
).json()
print latest_release
# Extract tag name
tagname = latest_release['tag_name']
# what platform are we on?
platform = sys.platform
if 'darwin' in platform:
    lib = "liblonlat_bng.dylib"
    url = 'https://github.com/urschrei/{project}/releases/download/{tagname}/{project}-{tagname}-x86_64-apple-darwin.tar.gz'
elif 'win32' in platform:
    lib = "lonlat_bng.dll"
    url = 'https://github.com/urschrei/{project}/releases/download/{tagname}/{project}-{tagname}-x86_64-pc-windows-msvc.zip'
else:
    lib = "liblonlat_bng.so"
    url = 'https://github.com/urschrei/{project}/releases/download/{tagname}/{project}-{tagname}-x86_64-unknown-linux-gnu.tar.gz'
# Construct download URL
fdict = {'project': project, 'tagname': tagname}
built = url.format(**fdict)

# Get compressed archive and extract binary
release = requests.get(built, headers={'Authorization':'access_token %s' % ghkey}, stream=True)     
fname = os.path.splitext(built)
content = release.content
if fname[1] == '.zip':
    so = cStringIO.StringIO(content)
    raw_zip = zipfile.ZipFile(so)
    raw_zip.extractall('convertbng')
else:
    fo = io.BytesIO(content)
    tar = tarfile.open(mode="r:gz", fileobj=fo)
    tar.extractall('convertbng')

extensions = Extension("convertbng.cutil",
                    sources=["convertbng/cutil" + suffix],
                    libraries=["lonlat_bng"],
                    include_dirs=['.', 'convertbng'],
                    library_dirs=['.', 'convertbng'],
                    # from http://stackoverflow.com/a/10252190/416626
                    # the $ORIGIN trick is not perfect, though
                    runtime_library_dirs=['$ORIGIN'],
                    extra_compile_args=["-O3"],
)

# Append correct binary to manifest.in
with open('manifest.in', 'a') as f:
    f.write('include convertbng/%s\n' % lib)

if has_cython:
    extensions = cythonize([extensions,])
else:
    extensions = [extensions,]

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
    ext_modules = extensions,
    long_description=readme
)
