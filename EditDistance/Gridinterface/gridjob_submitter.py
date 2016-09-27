import time, traceback, sys
import threading
import mylogger as log

class Jobsubmitter ( threading.Thread ):
    def __init__(self, jobs=[], logfile="gridmonitor.log"):
        #self.jobs = jobs
        self.submitted = []
        self.pending = jobs
        self.logfile = logfile
        self.wait_for_jobs = True
        self.sleep_period = 1 # seconds
        
        threading.Thread.__init__ ( self )

    def new_job(self,job):
        log.logprint(self.logfile, "Received job  "+str(job.toDict()))
        self.pending.append(job)

    def exit(self):
        self.wait_for_jobs = False

    def submit_jobs(self):
        while self.wait_for_jobs or self.pending != []: 
            if self.pending != []:
                j = self.pending.pop(0)
                t0 = time.time()
                log.logprint(self.logfile, "starting job  "+str(j.toDict()))
                j.execute() 
                duration = time.time()-t0
                log.logprint(self.logfile, "started job  "+str(j.toDict())+". \n Took "+str(duration)+" seconds")
                self.submitted.append(j)
                #self.pending.remove(j)
            #threading.wait(self.sleep_period)
    
    def cancel():
        self.pending = []
        self.wait_for_jobs = False

        
    def run(self):
        t_start = time.time()
        self.submit_jobs()
        total = time.time()-t_start
        log.logprint(self.logfile, "Job submitting done. Submitted %s jobs. Took %f seconds" % (len(self.submitted), total))
