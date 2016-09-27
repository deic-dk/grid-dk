import os

def cleanup():
    jobsPrefix = "job"
    jobsDir = "GeneratedJobs/"
#    os.chdir(jobDir)
    
    
    for root, dirs, files in os.walk(jobsDir, topdown=False):
        for f in files:
            fname = os.path.join(root,f)
            #if raw_input("remove "+f+"?") == "y":
            if verify(f):
                os.remove(fname)
                print "removing ",fname
        for d in dirs:
            dname = os.path.join(root,d)
	    if verifyDir(dname):
                os.rmdir(dname)
                print "removing dir ",dname
        
import string
def verify(name):
    return (name[-10:] == ".mvdscript" or name[-5:] == ".mRSL") and name != "test"

def verifyDir(name):
    print os.listdir(name)
    return (os.listdir(name) == [])
        


if __name__ == "__main__":
    cleanup()
