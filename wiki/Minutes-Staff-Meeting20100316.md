# Staff meeting 16/3-2010

Minutes by Jost

Status and planning meeting at NBI.

Attending: Frederik, Jost, Benjamin, Jonas

We aim at getting the portal ready for pilot users within the next few weeks.

## Features and web page polish (walkthrough)

 - Menu: replace "Docs" by "Help" (Jost)
 - Dashboard: include a link to our documentation ( code.google.com). This should be configurable as another "site" item. (Jonas)
 - Submit Job:
     - job type chooser: higher up in the page, should extend/reduce functionality (runtime env.s , target resources, ..?..)
     - planned: JS-based submission "wizard" - another submit style (care not to overload it) (Jost/Benjamin - postponed)
     - disable sandboxes => do not show the chooser on the submit page (Jonas)

 - Job Monitor: Page title "Job Monitor" (Jost)
 - Virtual Orgs:
	- remove Public Wiki, rename "private Wiki" to "Wiki" (Jost)
	- add confirmation to membership/ownership request actions + add some free text field in the JS dialog (Jost)
	- implement deletion (+ support for deleted VOs in statistics) (Jost)

 Remark: User-Cache sensitive to file deletion! (Jonas)
   (reports negative numbers for own files and dir.s after cleaning files on the server)
   Obstacle for leaving/deleting VOs, so should be fixed.

       - VO membership update from VOMS - implement, but priority very low (Jost)

 - Resources: remove "sandbox" field in table if disabled (Jonas)

 - Statistics: redesign postponed (will involve eliminating Usage Record files) (Jost - postponed)

## Documentation on code.google.com

Benjamin has added material, most of them are job examples. (Benjamin/all)

 - The examples should be concrete (should be able to copy/paste for a test)
 - We should flesh out one advanced example as a "tutorial".
 - Also useful: to create a downloadable zip archive for this use case

Molegro use case: ask molegro developers about license issues (Jonas)

## Plans and ToDos

 - define and document a consolidated "application suite" (runtime environments)
 - documentation on runtime env.s and on providing resources
 - test different browsers/platforms ( Firefox, Chrome, Safari, IE, Opera? )
 - stress test by massive job submission

## Bits and Pieces

### = Backends =

Frederik asked about the estimated effort for adding new backends to MiG (background: new cluster at Cern).

The MiG infrastructure is ready for binding Q-ing systems like torque/pbs by CLI scripts (already done in MiG for PBS).

### = Quick demo of ESS/McStas prototype =

Jost quickly showed a prototype of an application-specific framework, created using only private VO web pages and Javascript.

### = Certificates, "Getting started" for documentation =

The procedure for getting access to Grid.dk should be described as follows:

 - ask for a certificate (from the MiG or from the Nordugrid CA)
 - or, better: use/get a DanID "digital signature"
 - Then apply for DCSC membership to get access to more resources.

 - People in VOMS, with a NorduGrid certificate: have access

We consider returning to our Confusa solution as soon as wayf is online.

### = Javascript requirement =

 The new MiG web heavily requires Javascript. 
 Replace http redirect on start page by a JS check and JS redirect. (Jost)