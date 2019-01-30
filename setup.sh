#/usr/bin/env bash -e

# @Author: laborde
# @Date:   2019-01-30T08:47:10+01:00
# @Email:  qlaborde@evertygo.com
# @Last modified by:   laborde
# @Last modified time: 2019-01-30T13:15:10+01:00

# if [ ! -e "./config.ini" ]
# then
cp config.ini.default config.ini
# fi


VENV=venv

if [ ! -d "$VENV" ]
then

    PYTHON=`which python2`

    if [ ! -f $PYTHON ]
    then
        echo "could not find python"
    fi
    virtualenv -p $PYTHON $VENV

fi

. $VENV/bin/activate

pip install -r requirements.txt
