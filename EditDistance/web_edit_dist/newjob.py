#! /usr/bin/python

import cgitb, cgi, os, sys
import pickle
cgitb.enable()
import config
sys.path.append("../Gridinterface")
import miginterface as mig

def create_files_table():
    ref_dir = config.reference_files_directory
    ref_files = os.listdir(ref_dir)
    ref_files.sort(key=lambda x: os.stat(os.path.join(ref_dir, x)).st_atime)
    ref_files.reverse()
    htmlstr = "<table class='ref_match_files'>"
    table_header = "<tr><th>Filename</th><th>Size(MB)</th></tr>"
    
    htmlstr += table_header
    
    for rf in ref_files:
		filestat = os.stat(os.path.join(ref_dir, rf))
		file_size = filestat.st_size / float(1000000)
		file_time = filestat.st_atime
		row = "<td><span class='file'><u>%s</u></span></td><td> %.2f </td><td><img id='delete' src='images/Delete-icon.png' width='10' title='delete file' filename='%s'> </img></td> " % (rf, file_size, rf)
        
		htmlstr += "<tr>"+row+"</tr>"
    htmlstr += "</table>"
    return htmlstr
	    
def create_files_table_remote():
    ref_files = mig.ls(config.input_files_mig_directory)
    htmlstr = "<table class='ref_match_files'>"
    table_header = "<tr><th>Files</th></tr>"
    
    htmlstr += table_header
    
    for rf in ref_files[5:]: # the first 5 lines are header info
		#filestat = os.stat(os.path.join(ref_dir, rf))
		#file_size = filestat.st_size / float(1000000)
		#file_time = filestat.st_atime
        
		row = "<td><span class='file'><u>%s</u></span></td>" % rf
        
		htmlstr += "<tr>"+row+"</tr>"
    htmlstr += "</table>"
    return htmlstr

script_tags = """
<script type="text/javascript" language="javascript1.5" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.0/jquery.min.js" ></script>
<script type="text/javascript" language="javascript1.5" src="javascript/myscripts.js"></script>
<script type="text/javascript" language="javascript1.5" src="javascript/jquery_scripts.js"></script>
<link rel="stylesheet" type="text/css" href="https://dk.migrid.org/images/site.css" media="screen"/>

<link rel="stylesheet" type="text/css" href="images/css/ref_match.css" media="screen"/>


<link rel="icon" type="image/vnd.microsoft.icon" href="https://dk.migrid.org/images/favicon.ico"/>

"""

head_tag = "<head><title>start job</title> %s </head>" % script_tags
head = "<HTML>\n\t %s \n\t\t\n" % head_tag
if config.use_remote_inputfiles:
    files_table_html = create_files_table_remote()
else:
    files_table_html = create_files_table()
    
body = """ 
  <body onload="defaultName()">
  
  <div id="content" style="width:auto">
  <h1>Grid reference matching</h1>

<center>
    <form method="post" id="submitjob_form" action="grid_edit_distance_action_cgi.py" enctype="multipart/form-data" >
<table class="ref_match_submit" cellspacing='15' >
      
      <tr><td>Name </td> <td><input size="30" type="text" name="name" id="procname"> </td></tr>
      <tr><td>Input file </td><td> <input size="30"  type="text" name="inputfile" id="inputfile"> </td></tr>
      <tr><td></td><td><p id="browse"> <u>Choose reference file.....</u></p></td></tr>
      <tr><td colspan='2'><span id="files">%s</span></td></tr>
      <tr><td><input size="30"  type="hidden" name="input_file_url" id="file_url" value='%s'>
      <input size="30"  type="hidden" name="outputfile" id="outputname" ></td></tr>
       <tr><td></td><td></td></tr>
      <tr><td colspan='2'><center><input type="submit" value="Run edit distance" id="submit_button"></center></td></tr>
</table>
    </form>
          </center>
    </div>
    
    </body>
     """ % (files_table_html, config.input_files_url)
     
     
     
upload = """
     <br><br><br><hr><br>   
     <form method="post" action="uploadfile_cgi.py" enctype="multipart/form-data" >
     <input type="hidden" name="MAX_FILE_SIZE" value= "%i" />
      <p>Upload file : <input size="30"  type="file" name="uploadfile" id="uploadname"></p>
      
      <input type="submit" value="Upload">
    </form>
        
        
    <div id="filesold" >
    <a onclick=showFiles()> </a>
    </div>
  </body>
""" % (config.max_filesize)

tail = "\n</HTML>\n"

print "Content-type: text/html"
print 
print head
print body
print tail
