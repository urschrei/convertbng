#!/bin/bash
set -e -x
if [[ "$TRAVIS_OS_NAME" == "osx" ]]; then
    # install OSX
    source ci/travis_osx_steps.sh
    # install_name_tool -change /Users/travis/build/urschrei/lonlat_bng/target/x86_64-apple-darwin/release/liblonlat_bng.dylib @loader_path/liblonlat_bng.dylib $HOME/build/urschrei/convertbng/convertbng/cutil.so
fi
