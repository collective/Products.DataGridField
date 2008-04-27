#!/bin/sh
#
# A script to build gzip-archive from a product (Cygwin)
# Copyright Mikko Ohtamaa 2005
#
#
#
# This script is intended to do a product release archive.
# Script must be run in product's folder.
# 
# A new release tar.gz is placed in Products folder.
#

# Get product name from the current path
PRODUCT=`basename "\`pwd\`"`

# Tarball variable is the basename of a package
# TODO: How to lowercase a variable in Unix shell 
# 
TARBALL=$PRODUCT

# Read version from version.txt
# Note that versio.txt must not contain trailing new line
VERSION=`cat version.txt`

# Tar filename including version information
FULL_TARBALL=$TARBALL-$VERSION.tar.gz

#
# Clean Products directory from a colliding file
rm ../$FULL_TARBALL 

# Force user access rights
# In Windows environment there a+rx is missing causing problems
# when transferred to Linux
chmod -R a+rx ../$PRODUCT

# Create tar package
# - No compiled python files (with or withour debug information)
# - No folders images and fonts
# - No Paint Shop Pro thumbnial files
# - No Subversion version management files
cd .. ; tar --exclude=*.pyc --exclude=*-pyd --exclude=images --exclude=fonts --exclude=*.jbf --exclude=.svn -cvzf $FULL_TARBALL $PRODUCT
