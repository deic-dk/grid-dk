# Staff meeting 14/4-2009

Minutes by Frederik

Present: Benjamin, Jonas, Jost, Frederik

## Web sites

Frederik clarified that we will have 4 web sites associated with grid.dk:

 - an internal Wiki for sharing information on technical stuff, meeting minutes etc. - we can use the NBI Wiki for that
 - an external Wiki+issue tracker+code repo for providing technical information to users and admins - we can use the [grid-dk Google code site](http://code.google.com/p/grid-dk/)
 - a portal for user/group, file, software and job management
  - Functionality 1: register/login, file, job management
  - Functionality 2: VO, SW management, stats (who ran which jobs where) admin view, user view
  - regarding Plone, Trac etc. I suspect we're better off doing this from scratch – pulling in stuff from MiG, Lunarc, GridSphere, Django and what else we can use - the domain
  - [grid.dk](http://grid.dk) will be used as domain - I'm working on getting a server
 - a simple information site with pointers to the other 3 sites – the domain [grid.dk](http://grid.dk) will be used for this too

## Progress on tasks and what's next

### Jonas

 - MiG server documentation: progressing - will continue in interation with Jost who will follow docs to setup EC2 instant-on cluster
 - SW catalogue: MIG + ARC: format, tools: no progresss - will write document to clear thoughts, Frederik will send pointers to his stuff
 - Follow up on certs: get MiG/NG/TDC root cert installed on Ålborg MiG+ARC resources and Steno :-)
 - Investigate how extract DN-lists from VOMS and use them in MiG, see https://voms.ndgf.org:8443/voms/dcsc.dk/webui/admin/users/list

### Benjamin

Frederik presented plans for portal/single sign-on

 - Frameworks/tools: MiG, Lunarc, GridSphere, Django, ...
 - External services (mashup)
  - WAYF/SLCS – see (login via Statsbiblioteket) https://slcstest.uninett.no/slcsweb/ - end result: users login on web interface and end up with short-lived cert/key in browser and on disk (both optional)
   - Alternatively they simply log in and use portal (key/cert on server)
  - VOMS – find out how to extract DN-list
  - SGAS – find out how to extract usage stats
  - Grid home dir

Benjamin will start working on applet for generating key and cert request and getting the request signed by SLCS.

Frederik will put Benjamin in contact with Norwegian SLCS guy.

### Jost

 - Test clusters on Amazon: ARC, MiG: progress, but ARC is stuck with non-working gridftp - probably due to non-working reverse DNS lookup (required by Globus). Will pursue workaround: set up name server on the ARC server itself. MiG stuck because of lack of documentation - Jonas will provide this.
 - Accounting: SGAS - NDGF, Ålborg: no progress yet.

### Frederik

 - Server: Björn (NBI) will host one at the NBI
 - Payment of server and other stuff (EC2): working on getting a grid.dk project account
 - Internal Wiki (this one): working on adding us as users on the NBI Wiki (private)
 - Investigating VOMS, WAYF/SLCS

### Next meetings

It was decided in the future to have biweekly meetings at the NBI, Tuesdays at 14:00.

The next one is the 28/4-2009 and will sport demos of job GUI submission by Frederik and Benjamin.

The one 12/5 falls out because of the cloud mini-symposium held here at the NBI, where all are invited (14-18).