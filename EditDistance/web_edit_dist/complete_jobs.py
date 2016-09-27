#! /usr/bin/python

import cgitb, cgi, os, time, sys
import pickle
sys.path.append("../Gridinterface")
import miginterface as mig
cgitb.enable()
import config

def update(process):
#    for j in jobs:
  #      if not j["status"] in ["INIT", "FINISHED"]:
    #        j["info"] = mig.get_status([j["remote_id"]])[0]
      #      j["status"] = j["info"]["STATUS"]
    jobs = process["jobs"]
    active_jobs = filter(lambda x : not x["status"] in ["INIT", "STOPPED", "FINISHED"], jobs)
    #print active_jobs
    ids = [j["remote_id"] for j in active_jobs]
    #print ids
    info_list = []
    if ids != []:
        info_list = mig.get_status(ids)
    
    for i in info_list:
        #print i
        for j in jobs:
            if j["remote_id"].strip() == i["ID"].strip():
                j["info"] = i
                j["status"] = j["info"]["STATUS"]
    #print jobs
    
    done = True
    last_finished = 0
    for j in jobs:
        if j["status"] != "FINISHED":
            done = False
            break
        if last_finished < time.mktime(time.strptime(j["info"]["FINISHED"])):
            last_finished = time.mktime(time.strptime(j["info"]["FINISHED"]))
    
    if done and jobs != []:
        process["state"] = "finished"
        process["ended"] = time.strftime("%X %x", time.localtime(last_finished+3600)) # mig time an hour behind
    
    return process

def create_results_view2():
    status_files_dir = config.status_files_directory
    status_files = os.listdir(status_files_dir)
    job_list = []
    for sf in status_files:
        fname = os.path.join(status_files_dir, sf)
        filetime = os.stat(fname).st_ctime
        f = open(fname, 'r')
        job_info = pickle.load(f)
        f.close()
        
        job_info["created"] = filetime
        job_info["status_file_path"] = fname
        inactive_states = ["finished", "cancelled"]
        #print job_info["state"]
        if not job_info["state"] in inactive_states: # only update running processes
           #print "updating", job_info["state"]
            new_job_info = update(job_info)
            
            #if new_job_info != job_info: # only dump new info
            f = open(fname, "w")
            pickle.dump(job_info, f)
            f.close()
        #print  job_info["created"]
        job_list.append(job_info)
        
#    job_list.sort(key=lambda x : time.strptime(x["started"].split()[-1:], "%H:%M:%S %m/%d/%y"))
    job_list.sort(key=lambda x : x["created"])
                                      # time.strptime("01:24:22 01/14/10","%H:%M:%S %m/%d/%y")
#    html = show_result_view(job_list)

    html = create_procs_table(job_list)
    return html


def show_result_view(jobs):
    htmlstr = ""
    for j in jobs:
        htmlstr += str(j)
    return htmlstr


def create_procs_table(proc_info_list):
    htmlstr = "<table class='ref_match_job_view' border='0' cellpadding='10' cellspacing='0'>"
    table_header = "<tr> <th>Name</th><th>Input file</th><th>Started</th><th>Ended</th><th>State</th><th></th> </tr>"
    htmlstr += table_header

    for proc in proc_info_list:
        url_param = ""

        url_param = "status_file="+proc["status_file_path"]

        cancel_link = ""
        if proc["state"] == "running":
            cancel_link = "<a href='cancel.py?socket=%s&%s'> Cancel <a/>" % (proc["socket_file"],url_param)

        row = "<td> <a href='job_status_view.py?%s'>%s</a> </td><td> %s </td><td> %s </td><td> %s </td><td> %s </td><td>%s</td><td><img id='delete' src='images/Delete-icon.png' width='10' title='delete entry' filename='%s' name = '%s'> </img></td>" % (url_param, proc["name"], os.path.basename(proc["input"]), proc["started"], proc["ended"], proc["state"], cancel_link, proc["location"], proc["name"])

        htmlstr += "<tr>"+row+"</tr>"
    htmlstr += "</table>"
    return htmlstr

if __name__== "__main__":
   
    reload_interval = 20 # seconds
    print "Content-type: text/html"
    print
    meta = "<meta http-equiv='refresh' content='"+str(reload_interval)+"'>"
    head ="<HTML>\n\t<HEAD>"+meta+"""\n\t\t<TITLE>jobs</TITLE> \n\t\t
    <link rel="stylesheet" type="text/css" href="images/css/ref_match.css" media="screen"/>
    <link rel="stylesheet" type="text/css" href="https://dk.migrid.org/images/site.css" media="screen"/>
    <script type="text/javascript" language="javascript1.5" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.0/jquery.min.js" ></script>
    <script type="text/javascript" language="javascript1.5" src="javascript/jquery_scripts.js"></script>
    
    </HEAD>\n\t\t<BODY>\n
    
<div id="content" style="width:auto">
  <h1>Grid reference matching jobs </h1>
    
    """
    tail = "</div></BODY>\n</HTML>\n"
     
    print head
    html = create_results_view2()
    print html#"running jobs "+str(running_jobs)

    print tail

