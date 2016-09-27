#!/usr/bin/python

import datetime, time, os, string
import subprocess
import tarfile
import sys
import os
import shutil
import docklib.myLogger  as myLogger
import Configuration.dockingConfig as config
import docklib.timestamp as timestamp
from docklib.mvdScripting import createMvdScript
#    from ligandInfo import getLigandInfoFromJob
import docklib.ligandInfo as ligandInfo
import docklib.jobFragmentation as jobFrag
import docklib.resultHandle as resultHandle

#logfile = ""

class GBVDocker:
    def __init__(self, exec_mode):
        self.logfile = ""
        self.dock_resultdir = ""
        if  exec_mode == "local":
            import docklib.grid.localinterface as MiG
        elif exec_mode == "grid":
    #import MiGuserscriptsInterface as MiG 
            import docklib.grid.miginterface as MiG
            if not MiG.command_test():
                print "Could not execute remote MiG test command. "
                sys.exit()
            
        self.MiG = MiG
        self.init_dirs()
        self.cached_files = []
        
    def init_dirs(self):
        if not os.path.exists(config.dockworkingDir):
            os.mkdir(config.dockworkingDir)
        if not os.path.exists(config.dockingscriptsDir):
            os.mkdir(config.dockingscriptsDir)
        if not os.path.exists(config.resultDirectory):
            os.mkdir(config.resultDirectory)
        

    # note: use range() to make ligandIndexes
    def dockStart(self,ligandIndexes, ligandfile, targetfile, fragmentStrategy, numberOfRuns, jobsize, immediateDispatch=True, testseed=-1):
 

        myLogger.logprint(self.logfile,"****************Starting docking job****************")

        msg = "Ligand indexes:"+str(ligandIndexes)+", runs:"+str(numberOfRuns)+", job size:"+str(jobsize)+", fragmentation strategy:"+fragmentStrategy
        myLogger.logprint(self.logfile,msg)

        if testseed != -1:
            myLogger.logprint(self.logfile,"Using static seed:"+str(testseed)) 
 
        # fragment the docking procedure into jobs 
        #myLogger.logprint(self.logfile, "Fragmenting by "+fragmentStrategy)
        jobs = jobFrag.fragmentJobs(ligandIndexes, numberOfRuns, jobsize, fragmentStrategy)
        jobNr = 0

        myLogger.logprint(self.logfile, "Job fragmentation created jobs: "+str(jobs))

        #if config.runmode == "remoteMiG":
        #    dockCacheFiles(config.softwareDir)

        # jobs is a list of dictionaries that each contain a list of ligands and 
        # how many times they should be run
        num_jobs = len(jobs)
        for job in jobs:
                print job
                infostr = str(jobNr+1)+"of"+str(num_jobs)
                jobTag = "job"+infostr+"_"+self.dockId # not really an id but kind of
                temp_jobfolder = config.dockingscriptsDir+jobTag
                os.mkdir(temp_jobfolder)

                ligandsInJob, workinfo = ligandInfo.getLigandInfoFromJob(job, ligandfile)
                print "ligandinjob "+str(ligandsInJob)
                ligandfilename = config.ligandfilesPrefix+str(jobNr)+".mol2"
                
                job["workinfo"] = workinfo
                # create a file containing the ligands in the job
                specligandfile = ligandInfo.createLigandFile(ligandfilename, temp_jobfolder, job, ligandfile)
                # copy target file to job dir
                targetfilename = os.path.basename(targetfile)
                copyofTarget = temp_jobfolder+"/"+targetfilename
                shutil.copy(targetfile, copyofTarget)

                ligandfilename = specligandfile.split("/")[-1]
                # create a MVD script to be executed by MVD on the grid,
                # only uses static seed if specified in config
                #if os.path.exists()
                                
                mvdScript = createMvdScript(job, jobNr, temp_jobfolder, specligandfile, targetfilename, testseed)#specligandfile, copyofTarget)
                job["ligands"] = ligandsInJob
                
                # set output tar filename 
                outputfile = config.outputfilesPrefix+jobTag+".tar"
                
                # if set the script will be submitted immediately. Otherwise we proceed
                if immediateDispatch: 
                    # start job before proceeding
                    jobId = self.dockStartJob(mvdScript, specligandfile, copyofTarget, outputfile, temp_jobfolder, jobTag)	
                    job["outputfile"] = outputfile
                    job["jobId"] = jobId
                    
                jobNr += 1
        myLogger.logprint(self.logfile, "Started "+str(len(jobs)) + " jobs.")
        return jobs

    def dockStartJob(self,mvdScript, ligandfile, targetfile, outputFile, workingdir, jobtag):
        executableFiles = []
        inputfiles = [ligandfile, targetfile, mvdScript]
        mvd_bin = config.mvdProgram
        if config.use_mvd_RTE:
            mvd_bin = config.RTE_bin
            #inputfiles.append(config.license)
            inputfiles.extend(config.server_files)
        else:    
            inputfiles.extend(config.MvdInputFiles) # the program files
            executableFiles = [config.mvdProgram] # this is just to make it executable (chmod) 

        cmd1 = mvd_bin+" "+mvdScript+" -nogui"  
        #cmd1 = "echo hej"#"ls "+config.mvdProgram+" "+mvdScript + " > "+workingdir + "/docresTest.txt" # fake operation
        cmd2 = "cd "+config.dockingscriptsDir # output will be in workingdir 
        cmd3 = "tar -cf "+outputFile+" "+jobtag
        cmd4 = "mv "+outputFile+" ../../" # back to the root
        
        cmds = []
        cmds.append(cmd1)
        cmds.append(cmd2)
        cmds.append(cmd3)
        cmds.append(cmd4)

        
        
        #if not self.caching:
        #    inputfiles.extend(config.MvdInputFiles)
            #cachedfiles = []

        resource_specifications = config.MiG_resource_specs
        home_dir = "./"
        # start the MiG job
        jobId = self.MiG.create_job(cmds, inputfiles, executableFiles, home_dir,home_dir,output_files=[outputFile], cached_files=self.cached_files, resource_specs=resource_specifications, name=jobtag)

        return jobId

    # updates the status key in the job dictionary with a status dictionary from MiG
    def dockUpdateStatus(self,jobs):
        for j in jobs:
            #print j["jobId"]
            jobInfo = self.MiG.get_status([j["jobId"]])[0]
            j["status"] = jobInfo 
        return jobs

    def dockMonitor(self,jobs):
        jobsDone = []
        myLogger.logprint(self.logfile, "Started monitoring")
        while (True):
            try:
                time.sleep(config.pollFrequency)
                self.dockUpdateStatus(jobs)
                for j in jobs:
                    if j["status"]["STATUS"] == "FINISHED":
                        self.dockHandleOutput(j)
                        jobsDone.append(j)
                        jobs.remove(j)
                        myLogger.logprint(self.logfile, "Job "+j["jobId"]+" done. Ligands: "+ str(j["ligands"]))
                        
                if jobs == []:
                    myLogger.logprint(self.logfile, "All jobs completed")
                    break
                print "\n-----------------------------------------------------\n"
                self.dockPrintStatus(jobs)
                self.dockPrintStatus(jobsDone)
                
            except KeyboardInterrupt:
                self.dockCancelJobs(jobs)
                break

        return jobsDone

    def dockPrintStatus(self,jobs):
        for j in jobs:
            statusStr = "Job : "+j["jobId"]+"\t"+j["status"]["STATUS"]+"\n"+ str(j["ligands"]) + "\n"
            print statusStr

    def dockHandleOutput(self,job):
        output_file_local = config.resultDirectory+self.dock_resultdir+"/"+job["outputfile"]
        outputfile = self.MiG.get_output(job["outputfile"], output_file_local)
        #self.MiG.remove_files(job["outputfile"]) # delete output from MiG server. takes string or list
        myLogger.logprint(self.logfile, "Retrieved output file for job "+job["jobId"])
        main_result_file = os.path.join(config.resultDirectory, self.dock_resultdir)+"/"+config.dockingResultsFilename
        resultHandle.handleResult(outputfile,config.resultDirectory+self.dock_resultdir,  job["jobId"], main_result_file)

    def dockCancelJobs(self,jobs):
        for j in jobs:
            self.dockCancelJob(j)

    
    def dockCancelJob(self,job):
        success = self.MiG.cancel_job(job["jobId"])
        if success: 
            myLogger.logprint(self.logfile,"Cancelled job : "+job["jobId"])
        else:
            myLogger.logprint(self.logfile,"Unsuccesful cancellation of job :"+job["jobId"])


    def dockCacheFiles(self, files):
        user_home_dir = "./"
        self.MiG.upload_files(config.MvdInputFiles, user_home_dir, recursive=True)
        self.cached_files = files

    def dock(self,ligandIndexes, ligandfile, targetfile, fragmentStrategy, runs, jobsize, seed=-1, cmd="", caching=True):
        self.dockId = timestamp.generateFolderName()
        self.dock_resultdir = "grid_dock_"+self.dockId
        self.logfile = config.resultDirectory +self.dock_resultdir + "/"+config.logfile
        self.newCmd = cmd
        self.caching = caching
        if caching and not config.use_mvd_RTE:
            self.dockCacheFiles(config.MvdInputFiles)   
        self.cached_files.extend(config.server_files)   # instated to handle license file
        dockingJobs = self.dockStart(ligandIndexes, ligandfile, targetfile, fragmentStrategy, runs, jobsize, testseed=seed)
        self.dockMonitor(dockingJobs)

if __name__== '__main__':

    if "-help" in sys.argv or "--help" in sys.argv:
        print "Usage: python grid_docker.py <options>\n"+"Options: \n \t -l \t local execution\n\n"+"Note: You can edit Configuration/dockingConfig.py to customize grid docking procedures."
        sys.exit()

    if "-l" in sys.argv:
        exec_mode = "local"
    else:  
        exec_mode = "grid"
    
    ligandIndexes = range(0,config.num_ligands,1) # number of ligands to use. The indexes are used to extract ligands some the main ligand file ("compounds.mol2"). 

    ligandfile = config.ligands_file #"molecules/compounds.mol2"
    targetfile = config.protein_file#"molecules/target.mvdml"

    fragmentStrategy = config.fragmentStrategy
    runs = config.runs
    jobsize = config.jobsize

    docker = GBVDocker(exec_mode)
    docker.dock(ligandIndexes, ligandfile, targetfile, fragmentStrategy, runs, jobsize)


