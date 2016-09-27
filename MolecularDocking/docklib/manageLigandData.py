import ligandInfo

# jobs contain a list of job dictionaries with number of runs and ligand index
def createLigandFiles(jobs, ligandfile):
    for job in jobs:
        ligandinfo = getLigandInfoFromJob(job, ligandfile)
        job["ligandfile"] = createFile(, ligandIndexes, ligandfile)
        
# creates a file containing the ligands in ligands
def createFile(filename, ligandsInfo, ligandfile):
    ligandLines = []
    file = open(ligandfile, "r")
    lines = file.readlines()
    for l in ligandsInfo:
        s = l["lines"][0]
        f = l["lines"][1]
        lingandLines.append(lines[s:f])
    lFile = open(filename,"w")
    lFile.writelines(lingandLines)
    lFile.close()
    


