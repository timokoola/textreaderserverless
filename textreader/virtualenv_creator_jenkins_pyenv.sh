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

if [ ! -d $DEV_ENV ]; then
    pyenv virtualenv 3.6.1 textreader
    echo "Dev virtualenv created."
fi

if [ ! -f "$DEV_ENV/updated" -o $BASEDIR/requirements.txt -nt $DEV_ENV/updated ]; then
	pyenv activate textreader
    pip install -r $BASEDIR/requirements.txt
    python $BASEDIR/setup.py install
    touch $DEV_ENV/updated
    echo "Dev Requirements installed."
    pyenv deactivate
fi

