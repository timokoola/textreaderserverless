#!/bin/bash -e

BASEDIR=`dirname $0`
VIRTUALENVS_ROOT="$HOME/.pyenv/versions/3.6.1/envs"
DEV_ENV="$VIRTUALENVS_ROOT/textreader"
DEPLOYMENT_ENV="$VIRTUALENVS_ROOT/textreadermini"
. ~/.bashrc

if [ ! -d $VIRTUALENVS_ROOT ]; then
	mkdir -p $VIRTUALENVS_ROOT
	echo "created directory for virtualenvs"
fi

if [ ! -d $DEPLOYMENT_ENV ]; then
    pyenv virtualenv 3.6.1 textreadermini
    echo "Deployment virtualenv created."
fi

if [ ! -f "$DEPLOYMENT_ENV/updated" -o $BASEDIR/requirements_minimal.txt -nt $DEPLOYMENT_ENV/updated ]; then
    pyenv activate textreadermini
    pip install -r $BASEDIR/requirements_minimal.txt
    python $BASEDIR/setup.py install
    touch $DEPLOYMENT_ENV/updated
    echo "Deployment Requirements installed."
    pyenv deactivate
fi