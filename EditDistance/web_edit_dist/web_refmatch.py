#! /usr/bin/python

import cgitb, cgi, os, time, sys
cgitb.enable()
import config


print "Content-type: text/html"
print

head = """<HTML>\n\t<HEAD>\n\t\
<link rel="stylesheet" type="text/css" href="images/css/site.css" media="screen"/>
<link rel="stylesheet" type="text/css" href="https://dk.migrid.org/cert_redirect/.default.css" media="screen"/>

<link rel="icon" type="image/vnd.microsoft.icon" href="https://dk.migrid.org/images/favicon.ico"/>

 \n\t\t</HEAD>"""

print head

body = """
<body >
<div id="topspace">
</div>
<div id="toplogo">
<img src="https://dk.migrid.org/images/site-logo.png" id="logoimage" alt="site logo"/>
<span id="logotitle">
Minimum intrusion Grid <font size="2" face="Verdana" color="red"> RSLIS</font>
</span>
</div>
<div class="menublock">
<div class="navmenu">
<ul>
	<li  class="submitjob"><a href="newjob.py"  target="main"> Start new job</a></li>
	<li  class="jobs"><a href="complete_jobs.py"  target="main">View jobs </a></li>
	<li  class="files"><a href="files.html?path=%s" target="main"> File manager </a> </li>
	<li  class="dashboard"><a href="https://dk.migrid.org"> Back to MiG web site</a> </li>
</ul>
</div>
</div>

<iframe src="newjob.py" name="main" height="90%%" width="80%%" style="margin:4px" frameborder="0" scrolling="auto"></iframe>

<div id="bottomlogo">
<img src="/images/copyright.png" id="creditsimage" alt=""/>
<span id="credits">
2003-2010, <a href="http://www.migrid.org">The MiG Project</a>
</span>
</div>
<!-- <div id="bottomspace"></div>-->

</body>

""" % config.mig_RSLIS_directory

print body

tail = "\n</HTML>\n"
print tail

