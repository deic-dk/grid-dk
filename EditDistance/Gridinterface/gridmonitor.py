import time, traceback, sys
import threading
import mylogger as log
from miginterface import get_status


class Gridmonitor ( threading.Thread ):
    jobs =[]
    output_dir = ""
    def __init__(self, output_dir=".", jobs=[], logfile="gridmonitor.log"):
        self.output_dir= output_dir
        self.jobs = jobs
        self.logfile = logfile
        self.wait_for_jobs = True

        threading.Thread.__init__ ( self )

    def done_submitting(self):
        self.wait_for_jobs = False
        
    def add_job(self,job):
        self.jobs.append(job)
        
    def remove_job(self,job):
        self.jobs.remove(job)
        
    def all_finished(self):
        finished = True
        for j in self.jobs:
            finished = finished and j.isFinished() and j.output_ready
        return finished

    def all_cancelled(self):
        cancelled = True
        for j in self.jobs:
            cancelled = cancelled and j.isCancelled()
        return cancelled

    def running_jobs(self):
        #running = True
        for j in self.jobs:
            running = not j.isCancelled() and not j.isFinished()
            if running:
                return True
        return False

    def update(self):
        self.group_update()
#for j in self.jobs:
        #    j.update()

        
        """
        Takes advantage of the multi status call on mig. Warning: assumes that the return info from mig has the same order.
        """
    def group_update(self):
        active_jobs = []
        for j in self.jobs:
            if j.isActive():
                active_jobs.append(j)

#                job_ids.append(j.remoteId)
        job_ids = map(lambda j : j.remoteId, active_jobs)
        job_info_list = get_status(job_ids)
        for j in xrange(len(active_jobs)):
            active_jobs[j].info = job_info_list[j]
            active_jobs[j].status = active_jobs[j].info["STATUS"]
        

    def cancel_jobs(self):
        for j in self.jobs:
            j.cancel()
        log.logprint(self.logfile, "Cancelled "+str(len(self.jobs))+" jobs")

    def start_jobs(self):
        log.logprint(self.logfile, "Starting "+str(self.jobs)+" jobs : ")
        for j in self.jobs:
            j.execute() 
            log.logprint(self.logfile, "started job  "+str(j.toDict()))
        log.logprint(self.logfile, "Started "+str(self.jobs)+" jobs ")

    def start_monitor(self):

        while True:
            try:
                self.update()
                for j in self.jobs:
                    if j.isFinished() and not j.output_ready: # get results when job is done and output has not been downloaded
                        #j.getOutput(self.output_dir)
                        log.logprint(self.logfile, "Job finished : "+str(j.toDict))
                        
                
                if not self.running_jobs() and not self.wait_for_jobs:
                    log.logprint(self.logfile, "No more running jobs.")
                    break
                    
                self.print_jobs_summary()
                time.sleep(10)
            except KeyboardInterrupt:
                log.logprint(self.logfile, 'User initiated cancellation of jobs')
                self.cancel_jobs()
                return
            except:
                log.logprint(self.logfile, "Error. Calling...")
                log.logprint(self.logfile,traceback.format_exc())
                time.sleep(10)
                #self.cancel_jobs()
                #sys.exit(-1)
        
    def print_jobs(self):
        lines = ""
        for j in self.jobs:
            line = ""
            line = j.getId() + "\t"+j.getRemoteId()+"\t"+j.getStatus()+"\n"
            lines += line
        print lines, 
    
    def print_jobs_summary(self):
        lines = ""
        summary = {}
        job_status_list= [job.getStatus() for job in self.jobs]
        for j in job_status_list:
            try: 
                summary[j] += 1
            except KeyError:
                summary[j] = 1
        
        sum_str = "%i jobs in total. " % len(self.jobs)
        for key in summary: 
            sum_str += "%s %i. " %(key, summary[key]) 
        log.logprint(self.logfile, sum_str)
    
    def run(self):
        self.start_monitor()

if __name__=="__main__":
    test_monitor = Gridmonitor()
    test_monitor.run()
    #test_monitor.all_finished()
    #test_monitor.update()
    #test_monitor.cancel_jobs()
    #test_monitor.start_jobs()
    #test_monitor.start_monitor()
