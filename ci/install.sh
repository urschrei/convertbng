#!/bin/bash
set -e -x
if [[ "$TRAVIS_OS_NAME" == "osx" ]]; then
    # install OSX
    source ci/travis_osx_steps.sh
    before_install
    PIP_CMD install -r dev-requirements.txt
    PYTHON_EXE ci/pre_install.py
    PIP_CMD install --install-option="--no-cython-compile" cython
    PIP_CMD install python-coveralls
    PIP_CMD install nosexcover
    # install_name_tool -change /Users/travis/build/urschrei/lonlat_bng/target/x86_64-apple-darwin/release/liblonlat_bng.dylib @loader_path/liblonlat_bng.dylib $HOME/build/urschrei/convertbng/convertbng/cutil.so
fi
