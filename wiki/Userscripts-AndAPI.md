# grid.dk scripts

# MiG command-line tools and API

This section presents more advanced options for submitting jobs to the grid.dk server. If you are comfortable with the Linux command line and basic scripting, the tools can be useful for managing multiple jobs. If you're familiar with Python programming, the API can be useful. Notice that jobs are submitted to the grid.dk server, which then submits them via MiG or ARC to computing resources at the DCSC regional operation centers.

Requirements:

  - a valid grid.dk certificate
  - cURL command-line tool for transferring data
  - Python version 2.5 or higher

## User scripts

The user scripts are tools that can be used to submit jobs from the command line. The scripts aim to emulate some of the most popular linux bash commands. They can be downloaded [here](https://portal.grid.dk/cgi-bin/downloads.py). 

## miglib.py API

`miglib.py` is a python module that contains a set of functions corresponding to the user scripts. When developing grid applications, it enables the developer to process the data remotely before and after grid execution. This module is included with the download above. 

## Configuration

Just as when accessing grid.dk with a web browser, the scripts and API use secure communication in which the user is authenticated by her certificate. The scripts need to be able to locate the users certificate. This information must be placed in the file `miguser.conf` located in the directory `$home/.mig/`. 

Example of `$home/.mig/miguser.conf`:

```
migserver https://grid.dk # url of the grid.dk server
certfile ~/.globus/usercert.pem # path to user certificate
keyfile ~/.globus/userkey.pem # path to user private key
cacertfile # path to the CA certificate - leave this unset
password PASSWORD # password of the private key
```

Replace PASSWORD with the password to decrypt your private key.

Click [here](files/miguser.conf) to download the miguser.conf template.

## More information

For more information please visit 
http://dk.migrid.org/public/doc/user_scripts/MiG-user-scripts.html