# generated script from mRSL EXECUTE
echo 'Where are we?'
/usr/bin/env hostname
pwd

echo and HOME is .${HOME}.

echo and XDG_CONFIG_HOME is .${XDG_CONFIG_HOME}.

echo and XDG_CACHE_HOME is .${XDG_CONFIG_HOME}.

echo and GNUPGHOME is .${GNUPGHOME}.

echo "piping in yes to accept the key"
echo "yes | 0launch -c http://portal.grid.dk/0install/lame.xml --version"
yes | 0launch -c http://portal.grid.dk/0install/lame.xml --version

echo "now should go through without key questions"
echo "0launch -c http://portal.grid.dk/0install/lame.xml --version"
0launch -c http://portal.grid.dk/0install/lame.xml --version

echo "testing another feed"
echo "0launch -c http://portal.grid.dk/0install/gawk.xml --version"
0launch -c http://portal.grid.dk/0install/gawk.xml --version

# ensure success at the end
echo Done

