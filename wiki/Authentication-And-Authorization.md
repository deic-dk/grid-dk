# Getting started with grid.dk

# Introduction

Grid.dk uses the http secure (https) protocol for communication between users and the grid.dk server. To access the grid.dk web portal you need to have a trusted certificate imported in your browser.

# Getting a certificate trusted by grid.dk

 - First of all you must tell your browser to trust the grid.dk web server by clicking [here](http://ca.nordugrid.org/cacrt.crt).

 - Next you need to install a certificate grid.dk trusts in your browser. There are 4 ways of doing this - the first one is preferred:
  - **Terena Certificate Service** - the easiest way: just login on the [Terena EScience Portal](https://tcs-escience-portal.terena.org/) and generate a certificate. This is currently only possible for users from Copenhagen University, but extensions are planned.
  - <font color=gray>**Nordugrid**: 1) request a certificate from the [NorduGrid certificate authority](http://ca.nordugrid.org/) (CA) by following their instructions. 2) Wait for the CA to send you a signed certificate and import the certificate in your browser. You can find help for this [here](http://code.google.com/p/grid-dk/wiki/CertificateHelp).</font>
  - <font color=gray>**grid.dk catch-all CA**: 1) request a certificate from [here](https://portal.grid.dk/cgi-sid/reqcert.py). 2) Wait for the CA to send you a signed certificate and import the certificate in your browser. You can find help for this [here](http://code.google.com/p/grid-dk/wiki/CertificateHelp).</font>
  - <font color=gray>**DANID** (obsolete). If you have a Danish "Digital Signatur", you can use this.</font>

 - Now you should be able to access <a href="https://portal.grid.dk/">grid.dk</a>.

This is the main grid.dk dashboard. 

![](images/dashboard_screenshot_edited.jpg | width=800)


You can browse using the left-side menu and get acquainted with the portal. For further information, continue with our <a href="http://code.google.com/p/grid-dk/wiki/Documentation"> documentation </a>.


## DCSC membership

To access and use the DCSC sandbox resources, you should apply for membership of the DCSC virtual organization by clicking the https://portal.grid.dk/images/icons/add.png icon on the <a href="https://portal.grid.dk/cgi-bin/vgridadmin.py">virtual organizations page</a>.

![](images/getting_access_join_DCSC_cut.jpg | width=400)

# Common problems

If you encounter problems, please first have a look at the this <a href="http://code.google.com/p/grid-dk/wiki/HelpPage">help page</a>.