#!/usr/bin/python

import os, sys, time, pickle

import cgitb, cgi, socket
sys.path.append("../Gridinterface")
import miginterface as mig
cgitb.enable()
import config
from ref_frontend_script import communicate_with_proc

def load_page(text):
    reload_interval = 3                 
    hosturl = "/grid_edit_distance_action_cgi.py"
    meta_tag = ""#"<meta http-equiv=\"refresh\" content=\""+str(reload_interval)+";url="+hosturl+"\"/>"
    #<meta http-equiv="refresh" content="2;url=http://webdesign.about.com">
#"<meta http-equiv='refresh' content='"+str(reload_interval)+"'  url='google.com'>"
    head = "<HTML>\n\t<HEAD>"+meta_tag+"\n\t\t<TITLE>Grid edit distance calculator</TITLE> \n\t\t</HEAD>\n\t\t<BODY>\n"
    tail = "</BODY>\n</HTML>\n"

    print "Content-type: text/html"
    print 
    print head
    print text

    print tail

form = cgi.FieldStorage()
socketname = form["socket"].value
socketpath = os.path.join(config.socket_directory, socketname)
status = ""
if os.path.exists(socketpath):
    try:
        succes, status = communicate_with_proc(socketpath, config.job_cancel_req)
    except socket.error:
        os.remove(socketpath)
        status += "Socket deleted."    
else:
    status = "Process is no longer running."
    
if form.has_key("status_file"):
    status_file = form["status_file"].value
    f = open(status_file)
    status_obj = pickle.load(f)
    f.close()
    ids = [j["remote_id"] for j in status_obj["jobs"]]
    
    for i in ids:
        mig.cancel_job(i)
    
    for j in status_obj["jobs"]:
        if j["status"] == "INIT":
            j["status"] = "STOPPED"
   
    status_obj["state"] = "cancelled"
    f = open(status_file, "w")
    pickle.dump(status_obj, f)
    f.close()
    
    
t = time.time()    
load_page(status)
  #  time.sleep(2)

def parse_status_file(f):
    stat_file = open(f)
    lines = stat_file.readlines()
    statusstr = ""
    for l in lines:
        statusstr += l + "<br>"
    return statustr
