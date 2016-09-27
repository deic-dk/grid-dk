#import dockingConfig
def createMvdScript(job, Nr, jobDir, ligandfile, targetfile, seed=-1):
    #templatePath = "mvdScriptTemplate.txt"#self.mrsl_template_file
    if jobDir != "": 
        if jobDir[-1] != "/":
            jobDir += "/"

    #mvdtemplate = open(templatePath, "r")
    #scriptStr = mvdtemplate.readlines()
    #mvdtemplate.close()
    
    scoreAlgorithm  = "MolDockGrid" #"MolDock"
    searchFunction =  "MSE" #"MolDock" 

    scoreAlgorithmStr = "EVALUATORTYPE "+scoreAlgorithm+" \nEVALUATOR cropdistance=0;gridresolution=0.30;hbond90=true\n"

    searchAlgorithmStr = "OPTIMIZERTYPE "+searchFunction+" \nOPTIMIZER populationsize=50;cavity=true;creationEnergyThreshold=100;poseGenerator=10,10,30;recombine=true;maxsimplex=750;simplexsteps=300;simplexdistancefactor=1;clusterthreshold=1.00;keepmaxposes=5\n"
    settingsTemplate = "DOCKSETTINGS maxIterations=$iterations$;runs=$runs$;ignoreSimilarPoses=true;IgnoreSimilarPosesThreshold=1;MaxPoses=$maxposes$ \nLOAD $targetfile$ \nPREPARE bonds=ifmissing;bondorders=ifmissing;hydrogens=ifmissing;charges=ifmissing;torsiontrees=always;detectcofactors=false \nDOCK [File=$ligandfile$;index=$index$]\n"

    if seed != -1:
        seedstr = "RANDOM "+str(seed)+"\n"
        scoreAlgorithmStr += seedstr

    scriptName = "mvd"+str(Nr)+".mvdscript"
    mvdScript = open(jobDir+scriptName, "w")	
    mvdScript.write(scoreAlgorithmStr+searchAlgorithmStr)
    
    workInfo = job["workinfo"]

    for work in workInfo:
        newscriptStr = createScriptSnippetBasedOnRuns(work["runs"], work["ligands"], ligandfile, targetfile, settingsTemplate)
        mvdScript.write(newscriptStr)
        """
    for runs, ligands in job.iteritems():
	newscriptStr = createScriptSnippetBasedOnRuns(runs, ligands, ligandfile, targetfile, settingsTemplate)
	mvdScript.write(newscriptStr)
        """

    mvdScript.close()
    return jobDir+scriptName

  
def createScriptSnippetBasedOnRuns(runs, ligands, ligandFile, targetFile, templateStr, userSettingsDict={}):
    
    defaultSettings = {"iterations":2000, "maxposes":5}

    ligandIndexes = ""
    for l in ligands:
        ligandIndexes += str(l["index"]) + ","
        
    ligandIndexes = ligandIndexes[:-1]

    #for i in scriptStr:
    templateStr = templateStr.replace("$runs$", str(runs))
    templateStr = templateStr.replace("$index$",ligandIndexes)
    templateStr = templateStr.replace("$targetfile$", targetFile)
    templateStr = templateStr.replace("$ligandfile$", ligandFile)

    # if there is a user specified setting use it. Other wise use the default values
    for param, value in defaultSettings.iteritems():
	if userSettingsDict.has_key(param):
	    templateStr = templateStr.replace("$"+param+"$",str(userSettingsDict[param]))
	else: 
	    templateStr = templateStr.replace("$"+param+"$", str(value))
		
    #scriptStr.append(i)
    return templateStr


def formatJobs(joblist):
    formattedJobs = []
    for j in joblist:
        job = formatJob(j)
        formattedJobs.append(job)
    return formattedJobs

def formatJob(job):
    jobdict = {}
    for j in job:
        if jobdict.has_key(j["runs"]):
            jobdict[j["runs"]].append(j["ligand"])
        else: 
            jobdict[j["runs"]] = [j["ligand"]]
# Make ascending indexes
    for runs, ligands in jobdict.iteritems():
        jobdict[runs] = sorted(ligands)
    return jobdict        


"""  
def generateMigScript(mvdScript, moleculeFiles, jobDir, resourceSpecsDict={}, notifyEmail="", runtenv=""):

    staticInputFiles = [
    "MVD/misc/data/ElementTable.csv",
    "MVD/misc/data/PreparationTemplate.xml",
    "MVD/misc/data/Residues.txtW",
    "MVD/misc/data/RerankingCoefficients.txt",
    "MVD/misc/data/sp3sp3a.csv",
    "MVD/misc/data/sp2sp2a.csv",
    "MVD/misc/data/sp2sp3a.csv",
    "MVD/misc/data/bindinAffinity.mdm",
    "MVD/bin/vinter.license"]

    # loose the ".mvdscript", add ".tar"
    outputFile = "output_"+mvdScript[:-10]+".tar" 

    executeMvdCommand = "MVD/bin/mvd "+mvdScript+ " -nogui"

    mrsl = []
    mrsl.append("::EXECUTE::\n")
    mrsl.append("chmod 755 MVD/bin/mvd \n")
    mrsl.append(executeMvdCommand+"\n")
    #mrsl.append("cd MVD/bin \n")
    mrsl.append("tar -cf "+outputFile+" *.*\n")
	      #+ "--exclude vinter.license target.mvdml *.mvdscript compounds.mol2 \n")

    if notifyEmail != "":
       mrsl.append("\n::NOTIFY::\n")
       mrsl.append(notifyEmail+"\n")

    mrsl.append("\n::INPUTFILES::"+"\n")
    for path in staticInputFiles:
	mrsl.append(path+"\n")

    for file in moleculeFiles:
	mrsl.append(file+"\n")

    mrsl.append("\n::OUTPUTFILES::"+"\n")

    mrsl.append(outputFile+"\n")

    mrsl.append("\n::EXECUTABLES::\n")
    mrsl.append("MVD/bin/mvd \n")

    if resourceSpecsDict.has_key("mem"):
	mrsl.append("\n::MEMORY::\n")
	mrsl.append(resourceSpecsDict["mem"]+"\n")

    if resourceSpecsDict.has_key("disc"):
	mrsl.append("\n::DISK::\n")
	mrsl.append(resourceSpecsDict["disc"]+"\n")

    if resourceSpecsDict.has_key("CPUtime"):
	mrsl.append("\n::CPUTIME::\n")
	mrsl.append(resourceSpecsDict["CPUtime"]+"\n")               

    mrsl.append("\n::RUNTIMEENVIRONMENT::\n")                   
    mrsl.append(runtenv+"\n")

    #print string.join(mrsl)
    mrslName = "mig_"+mvdScript[:-10]+".mRSL"
    mrslFile = open(jobDir+"/"+mrslName, "w")
    mrslFile.writelines(mrsl)
    mrslFile.close()
    return mrslName

"""
#job = [{'runs': 4, 'ligand': 1}, {'runs': 2, 'ligand': 2}, {'runs': 2, 'ligand': 10}, {'runs': 2, 'ligand': 8}, {'runs': 2, 'ligand': 6}, {'runs': 2, 'ligand': 3}]

#formjob =  formatJob(job)
#jobtestdir = "mol_server_localtest/createscript"
#print formjob
#mvdscript = createMvdscript(formjob, 0, jobtestdir, "compounds.mol2", "target.mvdml")

#input = ["compounds.mol2", "target.mvdml"]

#generateMigScript(mvdscript, input, jobtestdir)
