This folder contains software for performing McStas compilation, 
simulation runs and data visualisation through a VGrid (Virtual 
Organisation) inside MiG (grid.dk customisation branch).

It is based on MiG middleware features and javascript, and requires
a working McStas installation on used resource. The latter is specified
as a runtime environment "MCSTAS_TOOLS" which defines McStas installation 
parameters.

Directory src/ contains required web pages and html fragments with 
javascript, a javascript helper module, and a perl script derived from
the McStas "mcdoc" tool, as well as two subdirectories assumed to exist
in the javascript. These files should be copied to the private web space
of a VGrid.
Directory misc/ contains Mcstas-material unrelated to the middleware.
Directory doc/ contains more documentation material.

(c) 2010 grid.dk. 
	Author:  Jost Berthold (berthold at diku.dk)
    License: GPL-2 (derived from McStas and MiG, see file COPYING)

