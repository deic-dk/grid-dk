# Staff meeting 5/10-2010

Minutes by Jost

Status and planning meeting at NBI.

Attending: Benjamin, Frederik, Jesper, Jost 

## General plans summary

 - Get in shape for/start with real users!
  - Access to resources
  - Invite (and support) pilot users
 - DCSC user conference **November** **9**: we should contribute

## Demo GridPilot

Gridpilot is a Java-based client application interfacing to different
Grid systems, developed by Frederik. 

### = Demoed functionality =

 - installer (including java runtime).
 - Credential management (test credentials built-in)
 - Backends: Nordugrid, SSH, GLite, GridFactory (which we used)
 - Example applications to get started
  - flac to mp3
  - Blast

### = Quick look at the concepts =

An *application* is a program or script (called an *executable*) and
job template together with a set of *datasets*.
A *dataset* can be extended with new files (conceptually. They can be
URLs as well), and can be output or input to *jobs*.
*Jobs* are defined following a template of the application, and
conceptually are part of their output destination datasets.
*Executables*, typically shell scripts, are specified together with
input and output files (using reserved identifiers like inputFiles,
nEvents etc.). 

A monitor functionality shows the jobs' progress for all submitted
jobs. 
Software requirements are resolved by using virtual machines in
GridFactory. Virtual machines can be reused for new jobs for a certain 
period to amortise the startup cost.

Gridpilot uses its own runtime environment concept, held in a purpose-made
XML catalogue which supports dependencies and includes virtual 
machines in its concepts. Some software is provided as tarballs 
or disk images, various concepts.

### = To use Gridpilot with Grid.dk =

 - Implement a MiG backend
 - showcase it at the DCSC user conference
 - Gridpilot as an added value:
  - can provide grid services to grid-illiterates (requires that we develop custom (Gridpilot-)applications for the user)

## Getting Resources

 - the ARC support in the portal still needs to be refined
  - job type vocabulary "batch" vs. "arc" still unfavourable
  - need to explicitly target ARC resources (using functionality similar to [arcresources.py](https://portal.grid.dk/cgi-bin/arcresources.py)). Need to extend MiG-code (ARC binding of MiG does not support choosing queues yet).
 - new 300 core cluster at NBI, tier 3
  - we cannot use it officially, it has been bought by a physics project
 - we have to consolidate access to Aalborg clusters
  - set up a meeting with Josva
  - we should (at the same time) have some pilot users ready
  - have resources and users ready for demo in November

## Checking documented "advanced" use cases, portal test drive

 - Jesper and Frederik tried out the described use cases
  - CA certificate file causes problems. We needs a **link** to **CommonErrors**
  - maybe switch to **.globus** as the standard location
  - provide a **.mig/miguser.conf** for **download** - use tildes (~) in this file
 - epistatis: **R** **package** problems (R not installed, need to check runtime env.)
 - epistasis/molegro: use **popen**, which causes deprecation warnings
 - **molegro** **license** needs to be updated
 - **epistatis** should provide all files for **download**
 - users should be able to copy-paste field contents of the examples
 - maybe the files could be provided in a (read-only) **group** **folder** on the server
 - there should be a section **Files** in every examples

 - maybe the wiki should include an "intermediate level" example?

 - Can we avoid new users getting "ssl handshake failure" as their greeting page?
  - solve by a redirect from the www.grid.dk start page to a dummy with optional certificate.

## Recently...

 - Jesper: SGAS VGrid extension, some fixes
 - Benjamin: simplified python mig library
 - Jost: some MiG fixes, resource debugging and maintenance
 - Frederik: development of Gridpilot

## Misc

 - ARC support: targeting specific resources (queues)
 - new SGAS database. We should have a look and update. Postponed for now.
 - WAYF / Terena: we are waiting.

## Action Items

 - talk to Brian about the user conference
 - set up a meeting with Josva about resources (and QoS)
 - check tier-1 access based on "dcsc.dk" membership
  - Nordugrid certificate (Jesper's new certificate)
  - Are MiG certificates/proxies accepted on the tier-1 cluster?
 - polishing the example pages as described above