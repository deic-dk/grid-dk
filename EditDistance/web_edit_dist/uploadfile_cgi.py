#!/usr/bin/python

import os, sys, time
import config
import cgitb, cgi
cgitb.enable()

form = cgi.FieldStorage()

head = "<HTML>\n\t<HEAD>\n\t\t<TITLE>file upload</TITLE> \n\t\t</HEAD>\n\t\t<BODY>\n"
tail = "</BODY>\n</HTML>\n"

print "Content-type: text/html"
print 
print head

##    load_page("input not valid")
 ##   sys.exit()
#refdir  = "ref_files/"
name = form["uploadfile"].filename
content = form["uploadfile"].value

#print outputfile
#print name
path = os.path.join(config.reference_files_directory, name)
f = open(path, "w")
f.write(content)
f.close()
print """File uploaded.  Go to <a href="newjob.py" target="main"> Start new job </a> Find it under 'Choose reference file.....' 
"""
#t = time.time()    
#load_page(out)
  #  time.sleep(2)
print tail
sys.stdout.flush()