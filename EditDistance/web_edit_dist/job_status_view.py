#! /usr/bin/python 

import cgitb, cgi, os, sys
from complete_jobs import update
import pickle
cgitb.enable()
import config

def create_jobs_view(status_file):
    f = open(status_file)
    job_info = pickle.load(f)
    #job_list.append(job_info)
    f.close()
    update(job_info)
#    html = show_result_view(job_list)
    html = create_jobs_table(job_info["jobs"])
    return html 


def show_result_view(jobs):
    htmlstr = ""
    for j in jobs:
        htmlstr += str(j)
    return htmlstr
 

def create_jobs_table(jobs):
    mig_home_url  = "https://dk.migrid.org/cert_redirect/"
    htmlstr = "<table cellspacing='3'>"
#entry = "<br>%s %s <a href='status_cgi.py?socket=%s'>%s</a>"
    table_header = "<tr><th>Id</th><th>Status</th><th>Queued</th><th>Executing</th><th>Finished</th><th>Output</th></tr>"
    htmlstr += table_header
    for j in jobs:
        #j = job.toDict()
        #row = "<th> %s </th><th> %s </th><th> <a href='%s'>%s</a> </th><th> %s </th><th> %s </th><th> %s </th>" % (proc["name"],proc["input"],proc["output"],os.path.basename(proc["output"]), proc["started"], proc["ended"], proc["finished"])
        queued = ""
        finished = ""
        executing = ""
        output_file = j["mig_output_files"][0].split()[-1] # only one output file
        
        job_info = j["info"]
        if job_info.has_key("QUEUED"):
            queued = job_info["QUEUED"]
        if job_info.has_key("FINISHED"):
            finished = job_info["FINISHED"]
            output_file = "<a href='%s'>%s</a>"% (mig_home_url+output_file,os.path.basename(output_file))
        else: 
            output_file = os.path.basename(output_file)
        if job_info.has_key("EXECUTING"):
            executing = job_info["EXECUTING"]
        

        row = "<td> %s </td><td> %s </td><td> %s </td><td> %s </td><td> %s </td><td> %s </td>" % (j["id"], j["status"], queued, executing, finished, output_file)
        
        htmlstr += "<tr>"+row+"</tr>"
    htmlstr += "</table>"
    return htmlstr




print "Content-type: text/html"
print 

reload_interval = 5 # seconds
meta = "<meta http-equiv='refresh' content='"+str(reload_interval)+"'>"
head ="<HTML>\n\t<HEAD>"+meta+"""\n\t\t<TITLE>jobs</TITLE> \n\t\t
    <link rel="stylesheet" type="text/css" href="https://dk.migrid.org/images/site.css" media="screen"/>
    <link rel="stylesheet" type="text/css" href="images/css/ref_match.css" media="screen"/>
    
    </HEAD>\n\t\t<BODY>\n
    
    <div id='content'>
    <h1>Job list</h1>
    """
tail = "</div></BODY>\n</HTML>\n"

print head
form = cgi.FieldStorage()
#print form
#filepath = ""
html = "no path"
#print form
if form.has_key("status_file"):
    filepath = form["status_file"].value
  #  print filepath
    html = create_jobs_view(filepath)
    
#link  = "<a href='status_cgi.py'>status</a>"

print html#"running jobs "+str(running_jobs)
#print link
print tail
