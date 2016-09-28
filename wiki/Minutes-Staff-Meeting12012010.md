# Staff meeting 12/1-2010

Minutes by Jonas


Status and planning meeting at NBI.

Attending: Frederik, Jost, Benjamin, Jonas


## Web UI Discussion

We discussed some points in relation to design thread from Jost and
Jonas.
 - Merge submit Job with Jobs page (popup/link from Jobs)
 - Make shell menu entry user-selectable and off by default
 - Consider tab based AJAX job submit walk through
 - AJAX enable field based submit to allow fold/unfold of fields
 - AJAX File selector for input and executables in fields submit
 - Downloads under Files or static download from doc

Simon will only have very limited time to fix bugs, so Jost and Jonas
will proceed with these AJAX heavy tasks. Hopefully the AJAX from file
and job manager will work as good templates.


## Zero Install and RTEs

We should consolidate on using zeroinstall for all MiG and ARC
RTEs. That is we require z-i on all resources and either include z-i
feed and pack with job or pull in the z-i apps on demand.
We should try to reuse the secure shared caching method to avoid transfer
overhead.
We should expect some support work related to creating z-i packages for
users, but the z-i online documentation is pretty good. So it will
likely be mostly related to getting the relocation working.


## Portal Consolidation

We need to consolidate the portal setup scripts and configuration. All
code should be included in grid.dk repo. We will begin merging back the
general components to migrid trunk and only keep the customization in
grid.dk branch: Jost and Jonas will start merging file manager, job
manager and shell into trunk.
We need to move official installation to port 443.


## MiG Shell

Find out why shell doesn't work for IceWeasel (Jonas). Only help and
list actions supported there.
We should make RPC API docs at some point.


## Portal Server Administration

We got unexpected reboots recently - Jost talked to the NBI admin.
It is not our task to update the server, this will mostly be automatic. In the future, NBI admins will inform us when a reconfiguration or a reboot is necessary.

## Apache Memory Problem

Apache on portal leaks like a sieve!
Check modules...


## Software Catalog

We should limit access per VO: For example use VO membership file as
access control and forward SSL envs in the apache proxy.
Add access file path and environment field to match against file entries.
Then we can match SSL DN field against VO list.


## User Projects

Benjamin is starting some user projects to get more focus on sandbox
users.
We discussed some of the parallelization details for one of the
projects. There are multiple solutions including using a database, map reduce
and manual splitting.