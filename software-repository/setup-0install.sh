#!/bin/sh
#
# Compile and install zero-install in user space.
# In case any dependencies are missing they are installed in user space, too.
#
# Usage: $0 [INSTALL_PATH [BUILD_DEPS]]
# Where INSTALL_PATH is the directory to install everything into and
# BUILD_DEPS is one of YES, NO or AUTO where auto means that the dependencies
# are checked and only built if missing (default is AUTO).
# On clusters with heterogeneous software on nodes it may be better to overrule
# local auto detection or run the setup script on the nodes.

# Install in home unless another destination is specified
DEST="$HOME"
if [ $# -gt 0 ]; then
    DEST="$1"
fi

# Auto detect dependency build requirement per default
BUILD_DEPS="AUTO"
if [ $# -gt 1 ]; then
    BUILD_DEPS="$2"
fi

#echo "Cleaning for build"
#rm -rf ${DEST}/zero-install ${DEST}/build

echo "Building in $DEST"
mkdir -p ${DEST}/zero-install/deps/usr ${DEST}/build || exit 1
export PATH=${DEST}/zero-install/deps/usr/bin:${PATH}
export LD_LIBRARY_PATH=${DEST}/zero-install/deps/usr/lib:${LD_LIBRARY_PATH}
echo "PATH set to $PATH"
echo "LD_LIBRARY_PATH set to $LD_LIBRARY_PATH"

if [ "$BUILD_DEPS" = "AUTO" ]; then
    echo "Auto detecting availability of zero install build dependencies"
    python -c 'import gobject' &> /dev/null
    DEPS_AVAILABLE=$?
    if [ $DEPS_AVAILABLE -eq 0 ]; then
	echo "Environment looks fine for building zero-install"
    else
	echo "Environment lacks one or more dependencies for building zero-install"
	BUILD_DEPS="YES"
    fi
elif [ "$BUILD_DEPS" = "YES" ]; then
	echo "Forcing build of zero-install dependencies"
elif [ "$BUILD_DEPS" = "NO" ]; then
	echo "Ignoring zero-install dependencies"
fi

if [ "$BUILD_DEPS" = "YES" ]; then
    echo "Building all zero install dependencies from source"
    PC_VERSION=0.23
    echo "Building pkg-config-${PC_VERSION}"
    cd ${DEST}/build && \
	wget -c http://pkgconfig.freedesktop.org/releases/pkg-config-${PC_VERSION}.tar.gz && \
	tar xzf pkg-config-${PC_VERSION}.tar.gz && \
	cd pkg-config-${PC_VERSION} && \
	./configure --prefix=${DEST}/zero-install/deps/usr && \
	make && make install || exit 1
    
    GETTEXT_VERSION=0.17
    PATCH_PATH="gettext-${GETTEXT_VERSION}-gcc-4.3-open-fix.diff"
    echo "Building gettext-${GETTEXT_VERSION}"
    cd ${DEST}/build && \
	wget -c http://ftpmirror.gnu.org/gettext/gettext-${GETTEXT_VERSION}.tar.gz && \
	tar xzf gettext-${GETTEXT_VERSION}.tar.gz && \
	cd gettext-${GETTEXT_VERSION} && \
	wget -c http://grid-dk.googlecode.com/svn/trunk/software-repository/${PATCH_PATH} && \
        patch -s -p0 < ${PATCH_PATH} && \
        rm -f ${PATCH_PATH} && \
	./configure --prefix=${DEST}/zero-install/deps/usr && \
	make && make install || exit 1
    
    GLIB_VERSION=2.20.5
    echo "Building glib-${GLIB_VERSION}"
    cd ${DEST}/build && \
	wget -c http://ftp.acc.umu.se/pub/GNOME/sources/glib/2.20/glib-2.20.5.tar.bz2 && \
	tar xjf glib-${GLIB_VERSION}.tar.bz2 && \
	cd glib-${GLIB_VERSION} && \
	./configure --prefix=${DEST}/zero-install/deps/usr && \
	make && make install || exit 1
    export PKG_CONFIG_PATH=${DEST}/zero-install/deps/usr/lib/pkgconfig:${PKG_CONFIG_PATH}
    export CPATH=${DEST}/zero-install/deps/usr/include:${CPATH}
    
    MAJOR=2
    MINOR=6
    PY_VERSION=${MAJOR}.${MINOR}.5
    echo "Building python-${PY_VERSION}"
    cd ${DEST}/build/ && \
	wget -c http://www.python.org/ftp/python/${PY_VERSION}/Python-${PY_VERSION}.tar.bz2 \
	http://www.python.org/download/releases/${PY_VERSION}/Python-${PY_VERSION}.tar.bz2.asc && \
	tar xjf Python-${PY_VERSION}.tar.bz2 && \
	cd Python-${PY_VERSION} && \
	./configure --prefix=${DEST}/zero-install/deps/usr && \
	make && make install || exit 1
    # Create symlink if it doesn't exist already
    ln -s python${MAJOR}.${MINOR} ${DEST}/zero-install/deps/usr/bin/python
    
    MAJOR=2
    MINOR=20
    PGO_VERSION=${MAJOR}.${MINOR}.0
    echo "Building pygobject-${PGO_VERSION}"
    cd ${DEST}/build/ && \
	wget -c http://ftp.acc.umu.se/pub/GNOME/sources/pygobject/${MAJOR}.${MINOR}/pygobject-${PGO_VERSION}.tar.bz2 && \
	tar xjf pygobject-${PGO_VERSION}.tar.bz2 && \
	cd pygobject-${PGO_VERSION} && \
	./configure --prefix=${DEST}/zero-install/deps/usr && \
	make && make install || exit 1
    echo "Re-testing with the recently built dependencies"
    python -c 'import gobject' || exit 1
    echo "Environment looks fine for building zero-install"
fi

    
ZI_VERSION="0.41"
echo "Building zero-install-${ZI_VERSION}"
mkdir -p ~/build && \
cd ~/build && \
wget -c http://sourceforge.net/projects/zero-install/files/injector/${ZI_VERSION}/zeroinstall-injector-${ZI_VERSION}.tar.bz2/download \
http://sourceforge.net/projects/zero-install/files/injector/${ZI_VERSION}/zeroinstall-injector-${ZI_VERSION}.tar.bz2.sig/download && \
(gpg --list-key 59A53CC1 &> /dev/null || gpg --recv-key --keyserver subkeys.pgp.net 59A53CC1) && \
gpg zeroinstall-injector-${ZI_VERSION}.tar.bz2.sig && \
tar xjf zeroinstall-injector-${ZI_VERSION}.tar.bz2 && \
cd zeroinstall-injector-${ZI_VERSION} && \
python setup.py install --home ~/zero-install --install-data ~/zero-install/local || exit 1
export PATH=${DEST}/zero-install/bin:${PATH}
export PYTHONPATH=${DEST}/zero-install/lib/python
echo "Install complete - now set environment to use zero-install:"
echo "export PATH=${PATH}"
echo "export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}"
echo "export PYTHONPATH=${PYTHONPATH}"
echo "... and optionally set environment to use newly built helpers"
echo "export PKG_CONFIG_PATH=${PKG_CONFIG_PATH}"
echo "export CPATH=${CPATH}"

exit 0
