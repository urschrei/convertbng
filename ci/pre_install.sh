  if [[ "$TRAVIS_OS_NAME" == "osx" ]]; then
    brew update
    brew install python
    pip install virtualenv
    virtualenv venv -p python
    source venv/bin/activate
    pip install pip --upgrade
    pip install nose
    pip install requests[security]
    python ci/pre_install.py
    # extractall works differently on OSX, apparently
fi

if [[ "$TRAVIS_OS_NAME" == "linux" ]]; then 
    sudo pip install requests[security]
    sudo python ci/pre_install.py
fi
