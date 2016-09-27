# test script for Zero-Install in ARC

echo 'Where are we?'
/usr/bin/env hostname
pwd

echo and HOME is .${HOME}.

echo and XDG_CONFIG_HOME is .${XDG_CONFIG_HOME}.

echo and XDG_CACHE_HOME is .${XDG_CACHE_HOME}.

echo and GNUPGHOME is .${GNUPGHOME}.

echo "Where is 0launch? Using /usr/bin/which..."
/usr/bin/which 0launch

echo "------------------------------ Trying a 0launch command:"
echo "0launch -c http://portal.grid.dk/0install/lame.xml --version"
0launch -c http://portal.grid.dk/0install/lame.xml --version

echo "------------------------------ Testing another feed:"
echo "0launch -c http://portal.grid.dk/0install/gawk.xml --version"
0launch -c http://portal.grid.dk/0install/gawk.xml --version

# ensure success at the end
echo
