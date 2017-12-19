#!/bin/bash -e

BASEDIR=`dirname $0`
VIRTUALENVS_ROOT="$HOME/virtualenvs"
DEV_ENV="$VIRTUALENVS_ROOT/textreader"
DEPLOYMENT_ENV="$VIRTUALENVS_ROOT/textreadermini"

if [ ! -d $VIRTUALENVS_ROOT ]; then
	mkdir -p $VIRTUALENVS_ROOT
	echo "created directory for virtualenvs"
fi

if [ ! -d $DEV_ENV ]; then
    virtualenv -q $DEV_ENV --no-site-packages --python=python3.6
    echo "Dev virtualenv created."
fi

if [ ! -f "$DEV_ENV/updated" -o $BASEDIR/requirements.txt -nt $DEV_ENV/updated ]; then
	. $DEV_ENV/bin/activate 
    pip install -r $BASEDIR/requirements.txt
    python $BASEDIR/setup.py install
    touch $DEV_ENV/updated
    echo "Dev Requirements installed."
    deactivate
fi


if [ ! -d $DEPLOYMENT_ENV ]; then
    virtualenv -q $DEPLOYMENT_ENV --no-site-packages --python=python3.6
    echo "Deployment virtualenv created."
fi

if [ ! -f "$DEPLOYMENT_ENV/updated" -o $BASEDIR/requirements_minimal.txt -nt $DEPLOYMENT_ENV/updated ]; then
	. $DEPLOYMENT_ENV/bin/activate 
    pip install -r $BASEDIR/requirements_minimal.txt
    python $BASEDIR/setup.py install
    touch $DEPLOYMENT_ENV/updated
    echo "Deployment Requirements installed."
    deactivate
fi