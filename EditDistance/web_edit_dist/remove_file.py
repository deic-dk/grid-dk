#!/usr/bin/python

import os, sys, time, pickle

import cgitb, cgi, socket
sys.path.append("../Gridinterface")
import miginterface as mig
cgitb.enable()
import config
from ref_frontend_script import communicate_with_proc
import json

def load_page(text):
    head = "<HTML>\n\t<HEAD>\n\t\t<TITLE>Grid edit distance calculator</TITLE> \n\t\t</HEAD>\n\t\t<BODY>\n"
    tail = "</BODY>\n</HTML>\n"

    #print "Content-type: text/html"
    print "Content-type: text/html"
    
    print 
    print head
    print text

    print tail


def json_page(text):
    print "Content-type: application/json"
    
    print 
    print text

form = cgi.FieldStorage()
filename = form["filename"].value
filepath = os.path.join(config.reference_files_directory, filename)
if form.has_key("format"):
	format = form["format"].value 

status = ""
if os.path.exists(filepath):
    try:
        os.remove(filepath)
        status = ("File deleted : %s" %filename, True)
    except os.error, msg:
		status ("Could not delete file %s : %s " % (filepath, msg), False)
			
else:
    status = ("File not found: %s" % filepath, False)

if format == "html":
	load_page(status[0])
if format=="json":
	json_msg = {"message":status[0], "status":status[1], "filename":filename}
	if not hasattr(json, 'dumps') and hasattr(json, 'write'):
		json.dumps = json.write
	json_page(json.dumps(json_msg))
	 
     