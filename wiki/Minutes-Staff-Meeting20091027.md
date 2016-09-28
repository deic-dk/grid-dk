# Staff meeting 27.10.2009

### = Attending: =

Frederik, Jonas, Jost

  - Frederik: We should focus on getting a demo of the portal up and running by the end of November where we're expected to show the functionality to DCSC
  - Frederik noticed that logging in with a NorduGrid certificate now works and jobs can be submitted on https://portal.grid.dk/
  - A crucial missing element is the SSO login via WAYF/Confusa - waiting for the Java app (Benjamin) and also for WAYF deployment on KU (Frederik will push for that).
  - ARC integration (Jost)
   - Jost runs a test installation on https://portal.grid.dk:8443/ - on which he demoed job submission on ARC resources (aau)
   - Software catalog: waiting for Jonas to finish 0install integration in MiG. After that the plan is to make MiG/0install SW available to ARC jobs submitted from the portal by shipping the tarball with the jobs (it will be cached on the resource) and adding a few lines to the beginning of the job script.
  - Usage records (Jost)
   - the new couchDB accounting work from Henrik (NDGF) looks promising
   - Jost demoed various views of a fictive usage DB
   - We decided to run our own couchdb using henriks software and get Danish ARC resources to log to both the NDGF DB and our DB (Frederik)
  - User home dirs (Frederik)
   - The new HTTPS/Webdav access method to NDGF storage was discussed: we could use it: NDGF states that they can redirect given namespaces to given storage pools, e.g. /grid/dk/ku to the pool at Steno (purely fictive example).
   - Users could then use fuse/davfs2 to mount their storage directly on their desktop.
   - The storage could also be mounted on the MiG server and presented via the file browser.
   - Mounting on the worker node is probably not feasible.
  - In general we agreed to look more into each other's work - in particular all will test the work done by Jost on the portal (his installation) and provide feedback.
  - We will also all try the portal and provide feedback to Jonas, Jost and Simon on usability improvements.

 