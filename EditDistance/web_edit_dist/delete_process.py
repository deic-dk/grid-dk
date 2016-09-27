#!/usr/bin/python

import os, sys, time, pickle

import cgitb, cgi, socket
sys.path.append("../Gridinterface")
import miginterface as mig
cgitb.enable()
import config
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

def clean_up(filepath):
    status = ""
    process = {}
    if os.path.exists(filepath):
        f = open(filepath, 'r')
        process = pickle.load(f)
        f.close()
    else:
        return ("Could not find status file", False)

    if not process["state"] in ["cancelled","finished"]:
        return ("Please cancel the process first", False)
    try:
        mig_output_path = os.path.join(config.output_files_mig_directory, process["output_dir"])
        if mig.path_exists(mig_output_path) : 
            succes = mig.remove_files([os.path.join(mig_output_path,"*")])
            succes = mig.remove_dir(mig_output_path)
        os.remove(filepath)
        return ("Entry removed", True)
    except Exception, msg:
        return ("Could not process %s : %s " % (filepath, msg), False)

def json_page(text):
    print "Content-type: application/json"

    print
    print text

form = cgi.FieldStorage()
filename = form["filename"].value
filepath = filename#os.path.join(config.status_files_directory, filename)
if form.has_key("format"):
    format = form["format"].value

status = clean_up(filepath)

if format == "html":
    load_page(status[0])
if format=="json":
    json_msg = {"message":status[0], "status":status[1], "filename":os.path.basename(filename), "name": os.path.basename(filename).strip(".pkl")}
    if not hasattr(json, 'dumps') and hasattr(json, 'write'):
        json.dumps = json.write
    json_page(json.dumps(json_msg))
