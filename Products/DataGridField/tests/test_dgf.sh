#!/bin/bash
#
# Simple example how to run unit tests for this product. 
#
# 	1. Fix ZOPE_HOME
#	2. Fix PYTHON
# 	3. Execute in tests folder
#
# Invoking unit test directly doesn't work anymore on Plone 2.5.1
# See http://plone.org/documentation/error/attributeerror-test_user_1_

PYTHON=/usr/bin/python2.4
ZOPE_HOME=/opt/Zope2.10
INSTANCE_HOME=`pwd`/../../..
SOFTWARE_HOME=$ZOPE_HOME/lib/python
CONFIG_FILE=$INSTANCE_HOME/etc/zope.conf
PYTHONPATH=$SOFTWARE_HOME
TEST_RUN=$ZOPE_HOME/bin/test.py

export PYTHONPATH

CMD="$PYTHON $TEST_RUN --help --config-file=$CONFIG_FILE --usecompiled -vp --package-path=$INSTANCE_HOME/Products/DataGridField Products.DataGridField"

CMD="$PYTHON $TEST_RUN --config-file=$CONFIG_FILE --usecompiled -vp --package-path=$INSTANCE_HOME/Products/DataGridField Products.DataGridField -m Products.DataGridField"

echo "Executing $CMD"

$CMD