# Staff Meeting 06.Oct. 2009


### = Attending: =

 - Frederik Orellana
 - Jonas Bardino
 - Benjamin Sedoc
 - Jost Berthold

 - Simon Lund, until 14:40


### = Demo, file interface for Portal (and MiG) =

   Simon showed a prototype of a new files interface, as a look-and-feel prototype for now. Similar to a "File Explorer", the functionality should be based on right-click menus (for now, only show, edit, and delete) and a directory tree navigation including upload and directory creation on the left.

   The interface is based on jQuery, a javascript library which already provides much of the needed functionality by default.

   Another task for the redesign is to present the job information in a table, including filters at the top. We have talked about the general ideas, but not the details.

### = Single Sign-On =

   Frederik reports that a different identity provider will have to be found for grid.dk, since the original partner now poses some problems.

   Furthermore, we discussed some technical details about the SSO application, in essence, where to store certificate and key ( .globus) and how to avoid overwriting existing certificates. In all, focus should remain easy usability for non-experts, so the location remains .globus . Probably a proxy certificate (with a long lifetime) should be generated at the same time automatically. Later integration will include this, and uploading the proxy to the portal server (or similar), but work for now should focus on eliminating problems and making the application run smoothly.


### = VGrid / Virtual Organisations in the portal =

   Members of the DCSC VO are now automatically imported into the portal server (created as users). Jonas also implemented functionality to automatically create a user when the certificate is accepted, but this is disabled for now.

   The MiG concept of VGrids will be (renamed and) used for the portal. The distinction into members and owners provides a natural "administration" role which, as far as we see, will fulfil our needs without any modification.

### = ARC backend work =

   Jost is working on integrating an ARC backend deeper into the MiG server. The server is running at portal.grid.dk on port 8443 (users need to be created for testing).
Status is, jobs can be submitted and monitored using the usual MiG interface. Next steps will be to present resource information for ARC resources and capture ARC runtime environments (probably as a special Sub-VGrid).

### = Software Repository =

   Jonas has built a prototype of a browsable software repository based on zero-install. Prepared software packages can be installed on demand on a resource from remote locations, enabling users to use an available software package on a range of resources without administrator interaction.

   Preparation of the packages is easy using tools provided by zero-install. It will also be possible for users (with appropriate skill level) to provide their own software packages. Some documentation material is checked in.

   The software catalogue will be an addendum to the available software on the resources when submitting a job. The exact way to integrate this into the MiG user interfaces requires further analysis.