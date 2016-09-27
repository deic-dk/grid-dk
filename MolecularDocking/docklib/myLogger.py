#import dockingConfig 
import os
import string

def log(file, s):

    if os.path.exists(file):
        writemode = "a"
    else: 
        dir = string.join(file.split("/")[:-1],"/")
        print dir
        os.mkdir(dir)
        writemode = "w"

    t = getTimeStamp()
    entry = t +" | "+s + "\n"
    logfile = open(file, writemode)
    logfile.write(entry)
    logfile.close()
    return entry

def logprint(logfile, s):
    msg = log(logfile, s)
    print "Debug: " +msg 

def getTimeStamp():
    import time
    (y,mo,d,h,m,s,_,_,_)= time.localtime()
    timestamp = "%i %i.%i %02i:%02i:%02i" % (y,mo,d,h,m,s)
    return timestamp
 
