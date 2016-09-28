# Staff meeting 10.11.2009

### = Attending: =

Benjamin, Jonas, Jost

Frederik couldn't attend so we took a quick status meeting. Perhaps we'll meet again next week if we need to sync - please coordinate by email. 


# New interfaces from Simon

Simon was going to demo but decided to work instead as the deadline moves closer fast.
Jost showed current status - it looks good with a lot of recent improvements but still some issues.
Files:
 - missing rename in right click menu
 - move cat and friends to advanced submenu
 - double click support to show/open?
 - head and other open new frame with slightly different style.
 - replace resubmit with submit
 - mkdir should use 'path' var instead of name (implicit input validation!)
 - upload file dialog not finished
 - drag and drop not finished?
 - probably other things...
Jobs:
 - replace links with buttons
 - rearrange a bit
 - ...

We should prioritize the list and let Simon proceed.
Demo is 9th og December! (Jost is going abroad on that date)


# Usage records

Jost displayed current status of usage stats with couchdb and charts/graphics from old job stats. Frederik will request actual usage stats from ARC jobs. Jost thinks we can demo some mockup - Jonas will provide mRSLs for this year for demo usage records.
Short term we don't care about access control for stats, but we may add it later.
We could at least anonymize user and resource IDs.
Live stats won't be available for the demo!


# SSO integration

Benjamin will write down some instructions for setting up SSO. Jost suggested creating a VM with middleware and SSO setup.
SSO works but autocreate has a problem with the broken DN format. We need to work on the input validation to allow the email address as part of the common name and possibly commas instead of slashes as field separators. Jost and Benjamin will investigate this possibly with input from Jonas. 
Jost is working on automating proxy upload and needs to investigate an SSL problem, but it is generally on track.

There's going to be some politics in getting the confusa certificates accepted on ARC resources.


# Software repository

Jonas displayed the suggested audio file recoding and conversion using the zero install feeds from the software repository and manual RTEs. The demo should use the raw $FLAC command to emphasize the RTE mechanism instead of hiding it all in a script.