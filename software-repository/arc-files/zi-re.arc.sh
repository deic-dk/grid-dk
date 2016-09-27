#!/bin/bash
#
# ENV/ZERO-INSTALL runtime environment script for Nordugrid ARC
#
# This ENV assumes installation of the zeroinstall-injector package,
# available in common Linux distributions, or at http://0install.net.
#
# Runtime environment scripts are called (bash source)
#   from NorduGrid ARC with argument 0,1 or 2.
# First call with argument "0" is made before the the batch
#   job submission script is written.
# Second call is made with argument "1" just prior to execution of the
#   user specified executable.
# Third "clean-up" call is made with argument "2" after the user
#   specified executable has returned.
#
# Made after a template by: 
# Olli Tourunen <olli.tourunen@csc.fi>
#
# Author:
#   Jost Berthold, grid.dk <berthold@diku.dk>

# Use these path extension variables if 0launch is not in the path
PATH_EXT=
PYTHONPATH_EXT=$ZEROINSTALL_HOME/lib/python

# Set this to the executing user's real home directory. 
# Configuration will be stored inside .config, .cache, and -gnupg
# Setup here is for "normal grid users" on benedict
USER_HOME=/user/grid

case "$1" in
0 ) 
    # Nothing here
;;
1 ) 
    # extend path in order to find 0launch
    if test x"$PATH_EXT" != x; then
        export PATH=$PATH:$PATH_EXT
    fi
    if test x"$PYTHONPATH_EXT" != x; then
        if test -z "$PYTHONPATH"; then
          export PYTHONPATH="$PYTHONPATH_EXT"
        else
          export PYTHONPATH="$PYTHONPATH:$PYTHONPATH_EXT"
        fi
    fi
    # set environment for zero-install to find keys and cache
    export XDG_CONFIG_HOME=$USER_HOME/.config
    export XDG_CACHE_HOME=$USER_HOME/.cache
    export GNUPGHOME=$USER_HOME/.gnupg

    # at least config and gnupg must exist
    if test ! -d $GNUPGHOME; then
	echo "Could not configure: GNUPGHOME ($GNUPGHOME) not found"
	exit 1
    fi
    if test ! -d $XDG_CONFIG_HOME/0install.net; then
	echo "Could not configure: CONFIG_HOME ($XDG_CONFIG_HOME) not found"
	exit 1
    fi
;;

2 )
    unset XDG_CONFIG_HOME XDG_CACHE_HOME GNUPGHOME
;;

* )
    # Now, calling argument is wrong or missing.
    # If call was made from NorduGrid ARC, it is considered
    # an error. If this script is to be used also to initialize
    # MPI environment for local jobs in cluster, raising error here
    # could be improper.
    return 1
;;
esac
