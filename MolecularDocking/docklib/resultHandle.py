import os, shutil, tarfile
#import dockingConfig
"""
# Moves and unpacks the the tar files containing job result files from mig user 
# directory to a result directory. 
def handleResults(userRootDir, jobTag, resultFiles, destinationDir, migOutputDir):
	#migUserDir = "/home/benja/mig/wwwuser/Benjamin_Richardt_Thomas_Sedoc/"
	#resultsDir = "dockingresults/"
	jobResultDir = userRootDir+"/"+destinationDir+"/"+jobTag
	resultRootDir = userRootDir+"/"+destinationDir
	#migOutputDirPath = userRootDir+"/"+migOutputDir
	
	
	if os.path.exists(resultRootDir):
	    print resultRootDir+" already exists"
	else:
		os.mkdir(resultRootDir)
		
	if os.path.exists(jobResultDir):
	    print jobResultDir+" already exists"
	else:
		os.mkdir(jobResultDir)
	
	resfiles = []	
	logfiles = []
	for resultFile in resultFiles:
		shutil.copy(migOutputDir+"/"+resultFile, jobResultDir)
		resTar = tarfile.open(jobResultDir+"/"+resultFile, "r")
		allfiles = resTar.getmembers()
		resTar.extractall(jobResultDir)
		jobId = resultFile[:-4]
		resTar.close()

		# rename all files to avoid overwriting
		for f in allfiles:
			oldname = f.name
			
			newname = oldname.replace(".", "_"+jobId+".")

			shutil.os.rename(jobResultDir+"/"+oldname, jobResultDir+"/"+newname)
			if oldname == "DockingResults.mvdresults":
				resfiles.append(newname)
				fixPoseReferences(jobResultDir+"/"+newname,jobId)
			if oldname[:9] == "ScriptLog":
			    logfiles.append(newname)
	if not resfiles == []:
            mergeMvdresultFiles(resfiles, jobResultDir)
	if not logfiles == []:
            mergeLogFiles(logfiles, jobResultDir)

"""
def handleResult(outputfile, resultDir, jobId, main_result_file):
    #print outputfile
    resTar = tarfile.open(outputfile, "r")
    allfiles = resTar.getmembers()
    print allfiles
    resTar.extractall(resultDir)
    resTar.close()
#    for f in allfiles:
 #       resTar.extract(f, resultDir+"/"+f.name.split("/")[-1])
   # resTar.close()
    
    

    mvdlog = "MVDScriptLog_main.txt"
    # rename all files to avoid overwriting
    resfiles = []
    logfiles = []
    jobTag = jobId.split(".")[0]
    for f in allfiles:
        if f.isdir(): # we only want the files
            continue
        
	oldname = f.name
	newname = oldname.replace(".", "_"+jobTag+".")
        newname = os.path.basename(newname) # remove subdirs
	print oldname, resultDir, newname
	#shutil.os.rename(resultDir+"/"+oldname, resultDir+"/"+newname)
        shutil.copyfile(resultDir+"/"+oldname, resultDir+"/"+newname)
	#if oldname.startswith("DockingResults") and oldname.endswith(".mvdresults"):
        if newname.startswith("DockingResults") and newname.endswith(".mvdresults"):
	    # update references to the pose files
	    fixPoseReferences(resultDir+"/"+newname,jobTag) 
	    # add the job result file to the total result file
            mergeToResultFile(resultDir+"/"+newname, resultDir,main_result_file) 

	if newname[:9] == "ScriptLog":
	    mergeToLogFile(resultDir+"/"+newname, resultDir, mvdlog)

# Concatenates to the '.mvdresults' file from the job to the total result file
def mergeToResultFile(file, resultDir, resultFilename):
	import string
#	resultFilename = resultDir+"/"+dockingConfig.dockingResultsFile

	rfile = open(file,"r") 
        lines = rfile.readlines()
	if not os.path.exists(resultFilename):
	    totalResultFile = open(resultFilename,"w") 
	     
	    # Save the header from the first result file
	    header = []
	    for line in lines:
		if line[0] == "#":
			header.append(line)
		else: 
			#last line of header
			header.append(line)
			break
            
            headerstr = string.join(header)
            
            # update reference to output dir
            headerstr = fixOutputDirReference(headerstr, resultDir)
            totalResultFile.write(headerstr)

            
        totalResultFile = open(resultFilename,"a")
        
        #remove the comments
        while lines[0][0] == "#":
                lines = lines[1:]

        #remove header
        lines = lines[1:]

        totalResultFile.writelines(lines)
			
	rfile.close()	
	totalResultFile.close()

# Finds and renames the references to the molecular pose files
def fixPoseReferences(filepath, jobId):
    import string

    if not os.path.exists(filepath):
        print "no such file", filepath
	return
	    
    mvdresultFile = open(filepath,"r")
    linelist = mvdresultFile.readlines()
    mvdresultFile.close()
    mvdresultFile = open(filepath,"w")
    for i in range(len(linelist)):
	linelist[i] = linelist[i].replace(".mol2", "_"+jobId+".mol2")
    mvdresultFile.writelines(linelist)
    mvdresultFile.close()
    #return linelist
  #  return newlines

def fixOutputDirReference(headerstr, result_dir):
    oldOutputdir = headerstr.split("Output Directory: ")[1].split(" ")[0] 
    newOutputdir = result_dir
    headerstr = headerstr.replace(oldOutputdir, newOutputdir)

    return headerstr

    
    

# Merges the current log file to the total log file located in dir
def mergeToLogFile(file, resultdir, mvd_log):
	logFilename = resultdir+"/"+mvd_log 
	#create the total result file by renaming the 
	if not os.path.exists(logFilename):
		shutil.copy(file, logFilename)
		return
	logFile = open(logFilename,"a") 
	
	file = open(file,"r")
	#if os.path.exists(resultFilename)
	lines = file.readlines()
	#remove the comments
	logFile.writelines(lines)
			
	file.close()
	logFile.close()


			
#file
# merge with total result file
#tarFiles = ["testresult0.tar"]
#handleResult("dockRes", "myJob", "testjobid")

#handleResults(".", "jobs_11_9_5_6_8_2008[1]", ["jobs_13_16_36_6_8_2008[1].tar", "jobs_13_16_36_6_8_2008[2].tar"], "mol_server_localtest/dockingresults", "mol_server_localtest")
