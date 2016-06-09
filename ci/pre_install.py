#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import io
import requests
import cStringIO
import zipfile
import tarfile

# We need to build the module using a Rust binary
# This logic tries to grab it from GitHub, based on the platform
print os.path.dirname(os.path.realpath(__file__))
# Get latest Binary from Github
# get GH access token from Travis
with open('key.txt', 'r') as f:
    ghkey = f.read().strip()
project = 'lonlat_bng'
latest_release = requests.get(
    "https://api.github.com/repos/urschrei/%s/releases/latest" % project,
    headers={'Authorization':'token %s' % ghkey}
).json()

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
    raw_zip.extractall('/Users/travis/build/urschrei/convertbng/convertbng/')
else:
    fo = io.BytesIO(content)
    tar = tarfile.open(mode="r:gz", fileobj=fo)
    tar.extractall('/Users/travis/build/urschrei/convertbng/convertbng/')
