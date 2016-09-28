# Staff meeting 17.11.2009

### = Attending: =

Frederik, Benjamin, Jonas, Jost, Simon


# SSO Integration

Benjamin demoed SSO integration...

There are still some issues preventing fully automated setup of certificate and CA. 
Import p12 cert and selecting password still requires popups. We discussed hard coding password, but apart from being as insecure as the proxy in /tmp it also prevents manual CLI use with the certificate.

Explorer still has some issues with certificate import: apparently it needs to be restarted after import.

Users with an existing certificate should not be offered SSO.
SSO users get created on tthe server with minimal access (Generic VGrid) and must request any additional membership. We discussed two way VOMS sync, but leave it for now. 


Punkt.KU should be WAYF enabled btw, but we may have to use Statsbiblioteket for the demo if we can't use Punkt.KU.


# AJAX interfaces to files and jobs

Simon demoed new interfaces.
There are still some bugs to weed out in the files interface:
 - Simon will continue with the ones in the AJAX code
 - Uploads using textarea return non-json (Jost, Simon and Jonas will check)
 - Default action for double click is to be decided (depends on mime header)
 - Perhaps we need a new page to mangle headers depending on file size and mime type
 - Discussion pointed to edit as default action, but it could depend on file

The new jobs page is nearly complete with all functionality in place. Perhaps still some small polishing. Icons or title text can be improved to be more telling. Consider right click menu with the advanced actions, and only keep cancel and resubmit as icons.
Consider bulk actions using tick boxes. The right click menu will have to be context sensitive to only map the relevant functions. Simon will decide which way the selection should work (tick boxes or mouse select)

Dashboard should be improved as discussed earlier: more job status and less docs. This is lowest priority.


# Usage statistics

It would be nice to display live statistics as a part of the demo.
Requires CouchDB and some Python Twisted which Jost will install in user space for the next meeting.


# Software Repository

Flac use case is not very scientific!

Benjamin will investigate Molegro or other scientific software, that we can demo instead.
Other possible targets would be Image group also providing their cluster as a resource, or something like BLAST or FFTW.
Benjamin and Jonas will coordinate the actual wrapping of the software into sw repo and RTE.