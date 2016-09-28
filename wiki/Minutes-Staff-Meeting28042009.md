# Staff meeting 28/4-2009

Minutes by Frederik

Present: Benjamin, Jonas, Jost, Frederik

## Progress on tasks and what's next

### Jost

Test clusters on Amazon: ARC, MiG

 - No progress on ARC - given up.
 - MiG reported to be working, but no jobs actually submitted.
--> Frederik asked Jost to see MiG through, i.e. to produce disk images that anyone can fire up to get a MiG cluster.||

Accounting: SGAS - NDGF, Ålborg

 - Jost reported on the structure of the system and some specific problems.
--> Frederik asked Jost to write a so-called JARM for MiG, allowing MiG to report usage to the NDGF SGAS server.
||ARC can already report to such a server. In the future, NDGF have agreed that the KU and AAU ARC installations will report usage to this server and grid.dk will be allowed to extract it. What remains, in order to obtain full usage reports, is then to extract (XML) records from the NDGF SGAS server and match these records with the DCSC DN-list extracted from VOMS.||

### Jonas

Documentation

 - Used input from Jost to write MiG documentation and fix bugs in MiG.
 - SW catalogue
  - Initial document with thoughts and ideas has been produced and sent around to all.
  - Follow up on certs - get MiG/NG/TDC root cert installed on Ålborg MiG+ARC resources and Steno
--> No progress reported --> please follow up
  - Investigate how extract DN-lists from VOMS and use them in MiG
--> No progress reported --> please follow up

### Benjamin

 - Benjamin is now in contact with Thomas Zangerl from PDC/KTH and Henrik Austad from Uninett. These two will work on the Confusa server, while Benjamin will work on the applet (or web start app).
 - Work on the applet is progressing well, Benjamin reported that it can produce an CSR and in principle upload it to Confusa.
 - As soon as we have a grid.dk server up and running, Benjamin will set up a Confusa test server.

### Frederik

 - Server: now coming very soon (in the next few days).
 - Payment of server and other stuff (EC2): still working on getting a grid.dk project account - prospects not too bright, we may have to send all bills to Brian individually.
 - Internal Wiki (this one): we're all added as users.
 - Attended meeting with NDGF on WAYF/SLCS, VOMS

### Demo by Benjamin

Benjamin demonstrated a nice GUI, tailored for his epistasis-analysing doctor to carry out his statistical analysis of gene/trait correlation.
 - It featured drop-down lists, etc. for setting input parameters to the jobs.
 - The jobs all act on the same input file - which is copied out to the worker node with every single job.
 - There was no discussion of which output these jobs produce, how and where it is stored and catalogued. - Benjamin: please comment.

Benjamin comment: Dr. Fenger has written the core statistics program which produces the output. He uses pure text files to store the data. For potential data mining it has been suggested that output data be stored in a database. However, along with a number of other improvements, this feature might exceed the current scope of the project.

Frederik commented that Benjamin's GUI and general implementation of the epistasis analysis constitutes a very nice piece of work. The usefulness for grid.dk is that it has been a learning experience for Benjamin. In the future this amount of work cannot be invested in a single 'client'. The aim of grid.dk is to put in place a system that allows many 'clients' to carry out their work on the DCSC resources. We don't have the manpower to give more than a very few this kind of treatment and therefore we have to produce something reusable.

### Demo by Frederik

Frederik was reorganizing his GUI and batch system, so there were no actual jobs submitted. Still, the message was conveyed that the ambition is to build something that is reusable across scientific domains and specific applications. Frederik will investigate the feasibility of running Benjamin's jobs with his GUI - GridPilot. This should be an excellent test of whether or not it actually makes sense to develop a common job-control GUI. It was also discussed to produce a MiG plugin for GridPilot. Notice that this work falls under the category 'advanced user interfaces' of the [roadmap](https://hep.nbi.dk/wiki/images/f/f9/Grid_dk_roadmap.pdf).