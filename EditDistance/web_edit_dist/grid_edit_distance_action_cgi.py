#!/usr/bin/python

import os, sys, time
import grid_edit_distance as ged
from ref_frontend_script import start_proc
import config

import cgitb, cgi
cgitb.enable()

def load_page(text):
    head = "<HTML>\n\t<HEAD>"+meta_tag+"\n\t\t<TITLE>Grid edit distance calculator</TITLE> \n\t\t</HEAD>\n\t\t<BODY>\n"
    tail = "</BODY>\n</HTML>\n"
    
    print "Content-type: text/html"
    print 
    print head

    print text

    print tail

def valid_form(form_obj):
    if form_obj.has_key("inputfile"):
        if not config.use_remote_inputfiles: # if we are using local input files, check if its there
            refdir  = config.reference_files_directory
            reffile = os.path.join(refdir,form_obj["inputfile"].value)
            if not os.path.exists(reffile):
                return (False, "file not found")
        return (True, "form accepted")
    else: 
        return (False, "form error. no inputfile field")
        #return True
    #return False
   
       

form = cgi.FieldStorage()

head = "<HTML>\n\t<HEAD>\n\t\t<TITLE>Grid edit distance calculator</TITLE> \n\t\t</HEAD>\n\t\t<BODY>\n"
tail = "</BODY>\n</HTML>\n"

print "Content-type: text/html"
print 
print head


(valid, msg) = valid_form(form)
if not valid:
    print msg
    print tail
    sys.exit()
##    load_page("input not valid")
 ##   sys.exit()
#refdir  = "ref_files/"
#if config.input_fil
if config.use_remote_inputfiles:
    ref_file = os.path.join(config.input_files_mig_directory,form["inputfile"].value)
else:
    ref_file = os.path.join(config.reference_files_directory,form["inputfile"].value)

outputfile = form["outputfile"].value
name = form["name"].value
#print outputfile
#print name
out = start_proc(name, ref_file, outputfile)
print out
#t = time.time()    
#load_page(out)
  #  time.sleep(2)
print tail

