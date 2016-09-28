# Staff meeting 27/4-2010

Minutes by Jost

Status and planning meeting at NBI.

Attending: Benjamin, Frederik, Jesper, Jost 

## Recent Activities

 - Jesper: implemented resource deletion.
Should be modified to only delete resources that are stopped/not executing jobs.

 - Frederik: got in touch with WAYF again about certificates.
The software and setup is still beta, but the testing environment has changed.

 - Benjamin: created many more wiki pages.
There are fully elaborated examplesnow, also involving the user scripts. Final polish will follow.

 - Jost: brought the ESS application (McStas) pages online on grid.dk.
         Needed modifications to VGrid web page service (to make ESS work)

## Plans / Misc

### Pilot Users

In June, the new DCSC sandbox user will receive their allocations. 
We will prepare a welcome letter from grid.dk, inviting them to use our portal.

Before that, we plan to invite 2 or 3 pilot users from the current grant holders.

### ARC resources of DCSC in Copenhagen

We aim, and are entitled to use a share of resources from dcsc (running ARC) 
in one way or the other.

The ARC job support in grid.dk is to be finished very soon.
 - The user has to decide whether ARC or "normal" MiG should be used.
    This is a conceptual problem (job scheduling differences) and can only be hidden.
 - ARC runtime environments have a different naming convention.
      We restrict ourselves to 0install-based runtime env.s and prefix the execution by the setup call.

Another solution (preferable, but not likely) is to get a MiG ssh account.

A similar solution would be to modify the ARC support and use only one server certificate

A central requirement will be that administrators should be able to view the usage, including the actual users. We could provide this via the usage statistics, but we go with the first solution.

For future ARC usage, the authorisation on ARC resources will be linked to DCSC VO membership, to keep things simple. Individual users might be allowed to access more resources, but the server will assume only DCSC-allowed resources.