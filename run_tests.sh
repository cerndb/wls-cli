#!/bin/bash

# Absolute path to this script. /home/user/bin/foo.sh
SCRIPT=$(readlink -f $0)
# Absolute path this script is in. /home/user/bin
SCRIPTPATH=`dirname $SCRIPT`

PYTHONPATH=$SCRIPTPATH/wls_rest/src/ python $SCRIPTPATH/wls_rest/src/wlscli/test/main.py
