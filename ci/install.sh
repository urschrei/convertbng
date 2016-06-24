#!/bin/bash
set -e -x
if [[ "$TRAVIS_OS_NAME" == "osx" ]]; then
    pip install pip --upgrade
    pip install -r dev-requirements.txt
    python ci/pre_install.py
    pip install --install-option="--no-cython-compile" cython
    pip install python-coveralls
    pip install nosexcover
    # install_name_tool -change /Users/travis/build/urschrei/lonlat_bng/target/x86_64-apple-darwin/release/liblonlat_bng.dylib @loader_path/liblonlat_bng.dylib $HOME/build/urschrei/convertbng/convertbng/cutil.so
fi
