

def fragmentJobs(ligands, runs, jobsize, fStrategy):
    jobs = []

    # fragment the docking procedure into jobs
    if fStrategy == "ligands":
        print "Fragmenting by ligands"
        jobs = createJobsBySingleRunMultipleLigands(ligandIndexes, numRuns, jobsize)
    elif fStrategy == "runs": 
        print "Fragmenting by runs"
        jobs = createJobsBySingleRunMultipleLigands(ligands, runs, jobsize)
    
    else : 
        print "Unkown strategy"        
    return jobs

def createJobsBySingleLigandMultipleRuns(ligands, runs, jobsize):
    size = 0
    joblist = []
    job = []
    for l in ligands:
        numRuns = 0
        for r in range(runs):
            numRuns += 1
            size += 1
            if size == jobsize:
                job.append({"ligand":l, "runs":numRuns})
                joblist.append(job)
                job = []
                size = 0
                numRuns = 0
        # Save the job created so far, if we're not done 
        if size > 0:
            job.append({"ligand":l, "runs":numRuns})

    # No more work, add the last job. 
    if size > 0: 
        joblist.append(job)
    return joblist


def createJobsBySingleRunMultipleLigands(ligands, runs, jobsize):
    size = 0
    joblist = []
    job = []
    initJob = []
    if jobsize > len(ligands) :
        for l in ligands: 
            initJob.append({"ligand": l, "runs":0})
        job = getInitList(ligands)
    #print initJob
    for r in range(runs):

        for li in range(len(ligands)):        
            size += 1
            if len(job) <= li:
                job.append({"ligand":ligands[li],"runs":1})

            else:
                job[li]["runs"] += 1               
            
            if size == jobsize:
                #job.append((l,1jobligands)
                joblist.append(job)
#                jobligands = []
                job = getInitList(ligands)
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
print createJobsBySingleLigandMultipleRuns([1,2,3,4], 4, 6)
#print createJobsBySingleLigandMultipleRuns(range(100000), 4, 6)
