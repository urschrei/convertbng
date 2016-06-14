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
platform = sys.platform
print platform

# Get latest Binary from Github
if not 'win32' in platform:
    # get GH access token from Travis
    with open('key.txt', 'r') as f:
        ghkey = f.read().strip()
elif 'win32' in platform:
    ghkey = os.environ['TARBALL_KEY']

project = 'lonlat_bng'
latest_release = requests.get(
    "https://api.github.com/repos/urschrei/%s/releases/latest" % project,
    headers={'Authorization':'token %s' % ghkey}
).json()

# Extract tag name
tagname = latest_release['tag_name']
# what platform are we on?
if 'darwin' in platform:
    lib = "liblonlat_bng.dylib"
    url = 'https://github.com/urschrei/{project}/releases/download/{tagname}/{project}-{tagname}-x86_64-apple-darwin.tar.gz'
elif 'win32' in platform:
    lib = "lonlat_bng.dll"
    url = 'https://github.com/urschrei/{project}/releases/download/{tagname}/{project}-{tagname}-x86_64-pc-windows-msvc.zip'
elif 'linux' in platform:
    lib = "liblonlat_bng.so"
    url = 'https://github.com/urschrei/{project}/releases/download/{tagname}/{project}-{tagname}-x86_64-unknown-linux-gnu.tar.gz'

# Construct download URL
fdict = {'project': project, 'tagname': tagname}
built = url.format(**fdict)
print "URL:", built
# Get compressed archive and extract binary
release = requests.get(built, headers={'Authorization':'access_token %s' % ghkey}, stream=True)     
fname = os.path.splitext(built)
content = release.content

path = os.path.join(os.environ['HOME'], "build/urschrei/convertbng/convertbng")

if fname[1] == '.zip':
    so = cStringIO.StringIO(content)
    raw_zip = zipfile.ZipFile(so)
    raw_zip.extractall(path)
else:
    fo = io.BytesIO(content)
    tar = tarfile.open(mode="r:gz", fileobj=fo)
    tar.extractall(path)

# with open("manifest.in", 'a') as f:
#     f.write("include convertbng/%s\n" % lib)
