import time
import os
import sys, random
import shutil
class Gridjob:
   staging_area_root = "/tmp/"
   Id = ""
   staged_files = []
   status = []
   output_files = []
   remoteId = ""

   def __init__(self, commands=[], input_files=[],specs={}, output_files=[], local=False):
      self.commands = commands
      self.specs = specs
      self.input_files = input_files
      self.staged_files = []
      self.Id = self.generateId()
      self.staging_area = self.staging_area_root+self.Id+"/"
      self.info = {}

      self.mig_dir = self.staging_area[1:] # stay in user space on mig server removing preceding "/" 
      self.output_files = output_files
      self.mig_output_files = [os.path.join(self.mig_dir,f) for f in self.output_files] # The file path on mig 
      
      if local:
         import localinterface as mig 
         self.mig_dir = self.staging_area 
      else:
         import miginterface as mig 
      self.mig = mig
      
      self.output_ready = False
      self.status = "INIT"

      self.stage() # prepare for execution
      

  #self.output_dir = output_dir
              

   def getId(self):
      return self.Id
   
   def getRemoteId(self):
      return self.remoteId
    
   def toDict(self):
      job_dict = {"commands":self.commands,"specs":self.specs,"input_files":self.input_files, "id": self.Id, "remote_id": self.remoteId, "output_files": self.output_files,  "output_ready": self.output_ready, "status" : self.status, "info": self.info, "mig_output_files":self.mig_output_files}

      return  job_dict

   def toFile():
        #def write_job_to_file(self,job, dest_dir):
      import pickle
        #num = 0
      filename = staging_area+self.Id.pkl+".pkl"
      output = open(filename, 'w')
      pickle.dump(job, output)
      output.close()

   def generateId(self):
      random.seed()
      rand= str(random.randint(0,int(time.time())))
      timestr = time.strftime("%H%M%S%d%Y")
      idnum = "gridjob"+timestr+rand
      return idnum


   def copy_files(self,input_files, dest_dir):
      files = []
      for f in input_files: 
         cp_filename = dest_dir+f.split("/")[-1]
         shutil.copyfile(f ,cp_filename)
         files.append(cp_filename)
        
      return files
            
      
   def stage(self):
        print "Staging job "+self.Id
        os.makedirs(self.staging_area)
      # do not need to create folders on mig because this i done through the submit script which unpack the inputfiles tar-ball
      # create dir on mig
        subfolders = self.staging_area.strip("/").split("/")
        #print subfolders
        path = ""
        for folder in subfolders:
            path += folder+"/"
            if not self.mig.path_exists(path):
                #print "dir", path
                self.mig.mk_dir(path)
        #sys.exit()

#            input_files = self.copy_files_to_local_working_dir(job["input_files"], job["job_dir"])
            #self.copy_files_to_local_working_dir(self.input_files, self.staging_area)
        for f in self.input_files: 
            cp_filename = self.staging_area+f.split("/")[-1]
            shutil.copyfile(f ,cp_filename)
            self.staged_files.append(cp_filename)

    #        job_file = self.toFile(, job["job_dir"])
      #      input_files.append(job_file)
        
            #job["input_files"] = input_files
         #print self.input_files
         #print self.staged_files
      
            #job["commands"].insert(0,"cd "+job["job_dir"])
            
        
   def execute(self):
      #mrsl_filename = self.staging_area+self.Id
      print "Executing job "+self.Id
      if self.commands == []:
         self.commands = ["echo 'No commands to execute...'"]
         
      # create and enter working directory on MiG resource(!) before we execute the actual commands. This ensures that output will be in the same dir on mig server. This makes it easier for get_file().
      cmds = self.commands
      cmds.insert(0,"mkdir -p "+self.mig_dir)
      cmds.insert(1,"cd "+self.mig_dir)

      output_list = map(lambda x: self.mig_dir + x, self.output_files)

      self.remoteId = self.mig.create_job(exec_commands=cmds, input_files=self.staged_files, executables=[], local_working_dir=self.staging_area, mig_working_dir=self.mig_dir,output_files=output_list, cached_files=[], resource_specs=self.specs)
            #job["started"] = self.get_time()
        #log(self.logfile,"Job created. Id :"+job["id"])
      #print self.remoteId
      self.status = "SUBMITTED"

   def update(self):
      #print "updating job "+self.Id
      if self.status == "INIT":
         print "cannot update yet. "
         return
      #new_status = False
        #job_ids = map(lambda x : x["id"], jobs)
        #for j in jobs:
            #print j["id"]if j
        #print job_ids
        #job_info_list = self.self.mig.get_status(job_ids)
      
      job_info_list = self.mig.get_status([self.remoteId])
        
        #if len(job_info_list) != len(job_ids):
         #  print str(job_info_list)
          # print str(jobs)
          # raise Exception("Critical job management error.  Job list lengths.")
        
        #for i in range(len(jobs)):
        #jobs["status"] = job_info_list[i]
      self.info = job_info_list[0]
      self.status = self.info["STATUS"] #
      #print job_info_list
      #print self.info
      #print self.status
        #if jobs[i]["status"]['STATUS'] == 'FINISHED':
        #  jobs[i]["finished"] = self.get_time()
        
            #print jobs[i]["id"], job_info_list[i]["ID"]
        #        map(lambda x : x["id"]=)
        
       # if not j.has_key("status") or jobInfo["STATUS"] != j["status"]["STATUS"]:
       #         j["status"] = jobInfo
        #        newStatus=True
        #if newStatus:
        #    self.PrintStatus(jobs)
        #return jobs

   def getStatus(self):
      return self.status
   
   def getOutput(self, destdir):
        #import resultHandle

      if destdir[-1] != "/":
         destdir +="/" 
        #for f in job["output_files"]:
        #    output_filename =  f
      outputfiles = []
      for output_file in self.output_files:
         retrieved_file = self.mig.get_output(self.mig_dir+output_file, destdir+output_file) # copy outputfile from migserver userdir to local dest userdir
         outputfiles.append(retrieved_file)
#log(self.logfile, "Retrieved output file for job "+job["id"],self.debug_mode)
              #print "opening ", destDir+filepath, "to", destDir
      #files.append(outputfile)
      self.output_ready = True
      return outputfiles

   def isFinished(self):
      return (self.status == "FINISHED")

   def isCancelled(self):
      return (self.status == "CANCELED") # misspelled intentionally

   def isActive(self):
      inactive_states = ["INIT", "CANCELED", "FINISHED"]
      active = not self.status in inactive_states
      return active 

   def cancel(self):
      self.mig.cancel_job(self.remoteId)
      if self.status == "INIT":
        self.status = "CANCELED"
      
   def clean_up(self):
         ""#files = []
         #files.append(self.input_files)
         

   def clean_up_job(self):
        #filepaths = []
        job_files = []
        job_files.extend(job["input_files"]) # r files
        if job["status"]["STATUS"] == "FINISHED":
            outputfile = job["job_dir"]+job["output_files"][0]
            job_files.append(outputfile)
        
        log(self.logfile, "Cleaning up for job (id:"+job["id"]+")")
        self.mig.remove_files(job_files)
        #self.remove_local_files(job_files)
               
        # locally 
#        if job["status"]["STATUS"] == "FINISHED":
 #           os.remove(job["output_files"][0])
        
        self.mig.remove_dir(job["job_dir"]) # directory
        os.rmdir(job["job_dir"])


def test():
   numjobs = 1
   jobs = list()
   cmds = ["echo hejsa > out.txt"]
   outputfile = "out.txt"
   for i in range(numjobs):
      job = Gridjob(commands=cmds, output_files = [outputfile], local=False)
      job.stage()
      job.execute()
      jobs.append(job)

   while True:
      for i in range(numjobs):
         time.sleep(3)
         job.update()
         print job.getStatus()
         print job.isFinished()
         if job.isFinished():
            job.getOutput(".")
            sys.exit()

if __name__ == "__main__":
   test()   
