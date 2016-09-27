import myLogger

def fragmentJobs(ligands, runs, jobsize, fStrategy):
    jobs = []

    # fragment the docking procedure into jobs
    if fStrategy == "ligands":
        #myLogger.logprint("Fragmenting by ligands")
        jobs = createJobsBySingleLigandMultipleRuns(ligands, runs, jobsize)
    elif fStrategy == "runs": 
        #myLogger.logprint("Fragmenting by runs")
        jobs = createJobsBySingleRunMultipleLigands(ligands, runs, jobsize)
    
    else : 
        #myLogger.logprint("Unkown strategy") 
        return
    #myLogger.logprint("Fragmentation: "+str(jobs))
    print jobs
    formattedJobs = reformatJobs(jobs)
    return formattedJobs

def createJobsBySingleLigandMultipleRuns(ligands, runs, jobsize):
    size = 0
    joblist = []
    job = {}
    for l in ligands:
        #numRuns = 0
        for r in range(runs):

            size += 1
            if job.has_key(l):
                job[l] += 1
            else: 
                job[l] = 1
            
            if size == jobsize:
                
                #job.append({"ligand":l, "runs":numRuns})
                joblist.append(job)
                job = {}
                size = 0
                #numRuns = 0
        # Save the job created so far, if we're not done 
        #if size > 0:
        #    job.append({"ligand":l, "runs":numRuns})

    # No more work, add the last job. 
    if size > 0: 
        joblist.append(job)
    return joblist


def createJobsBySingleRunMultipleLigands(ligands, runs, jobsize):
    size = 0
    joblist = []
    job = {}
#    initJob = []
    #if jobsize > len(ligands) :
        #for l in ligands: 
            #initJob.append({"ligand": l, "runs":0})
    #    job = getInitList(ligands)
    #print initJob
    i = 0
    direction = 1
    for r in range(runs):

        for l in ligands:        
            size += 1
            key = ligands[i]                            

            if job.has_key(key):
                job[key] += 1
            else: 
                job[key] = 1 
                
            
            #if len(job) <= li:
            #    job.append({"ligand":ligands[li],"runs":1})
                
            
            #else:
            #    job[li]["runs"] += 1               

            
            i += direction
            
            if i == len(ligands) or i == -1:
                direction *= -1    
                i += direction
                
            
            if size == jobsize:
                #job.append((l,1jobligands)
                joblist.append(job)
#                jobligands = []
                job = {} #getInitList(ligands)
    #            print initJob
     #           print job
                size = 0
          
    # No more work, add the last job. 
    if size > 0:
 #       job.append(jobligands)
        joblist.append(job)
    return joblist
    
def getInitList(ligands):
    list = []
    for l in ligands:
        list.append({"ligand":l,"runs":0})
    return list


def reformatJobs(joblist):
    formattedJobs = []
    for j in joblist:
        job = reformatJob(j)
        formattedJobs.append(job)
    return formattedJobs

"""def reformatJob(job):
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
def reformatJob(oldjob):
    job = {}

    # Make ascending indexes
    for ligand, runs in oldjob.iteritems():
        if not job.has_key(runs):
            job[runs] = [ligand]
        else: 
            i = len(filter(lambda x : x < ligand, job[runs]))
            job[runs].insert(i,ligand)
    return job   



"""
    def createJobsBySingleRunMultipleLigands(ligands, runs, jobsize):
        size = 0
        joblist = []
        job = []
        jobligands = []
        oldnumRuns = jobsize / len(ligands) + 1

        for j in range(len(ligands)*runs/jobsize):
            numRuns = 0
            starti = jobsize*j % len(ligands)
            for n in range(len(ligands)):        
                #numLigands += 1
                li = (starti+n) % len(ligands)

                numRuns = (jobsize-li) / len(ligands) + 1 
                print li, numRuns

                size += numRuns
                # if this ligand must be run a new number of times,
                # we save the other ligands and proceed
                if oldnumRuns != numRuns:
                    job.append((oldnumRuns, jobligands))
                    oldnumRuns = numRuns
                    jobligands = []

                jobligands.append(ligands[li])

                if size == jobsize:
                    job.append((numRuns, jobligands))
                    joblist.append(job)
                    job = []
                    size = 0
                    numRuns = 0


            #joblist.append(job)

        print joblist
                #% len(ligands) jobsize/len(ligands)+1

"""

            


#hej = (1,3)
#hej[1] = 2
#print hej[1]

            
#print createJobsBySingleRunMultipleLigands([1,2,3,4], 4, 6)
#print createJobsBySingleLigandMultipleRuns([1,2,3,4], 4, 6)
#print createJobsBySingleLigandMultipleRuns(range(100000), 4, 6)
