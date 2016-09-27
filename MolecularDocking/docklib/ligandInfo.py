
# two getLigandInfo() with differing input formats 
# getLigandInfo() outputs a list of dictionaries with {"name", "atoms", "bindings"}

import string

# reads molecule data and returns name, atoms, binding and number of
# lines to the next molecule
def getNextMol(index, ligandsStrs):
    beginTag = "@<TRIPOS>MOLECULE\r\n"
    miscLines = 9
    #print index, ligandsStrs[index]
    if ligandsStrs[index] != beginTag and index < len(ligandsStrs):
	print "Error : " +ligandsStrs[index]
	return "empty", -1, -1,-1

    #for i in range(index,len(ligandsStrs)):
    i = index
    if ligandsStrs[i] == beginTag:
	molName = ligandsStrs[i+1]
	molSpecs = string.split(ligandsStrs[i+2]," ")
	#print molSpecs
	numAtoms = int(molSpecs[1])
	bindings = int(molSpecs[2])
        nextIndex = miscLines + numAtoms + bindings
    return molName,numAtoms,bindings, nextIndex
    


# linear search by molecule index
def getLigandInfo(first, last, ligandsFile):
    beginTag = "@<TRIPOS>MOLECULE"
    path = ""
    
    ligandsFile = open(path+ligandsFile, "r")
    ligandStr = ligandsFile.readlines()
    cs = 0
    for l in ligandStr:
        cs += len(l)
    #(name,at,bi,index) = getNextMol(0,ligandStr)
    #print name, at, bi, "index :"+str(index)
    lineIndex = 0
    numMol = 0
    #print first, last
    ligands = []
    while(lineIndex < len(ligandStr)):
        name,at,bi,i = getNextMol(lineIndex,ligandStr)
        #name,at,bi,i = getNextMol2(ligandsFile)
        #        print "line"+str(lineIndex)+": ", name, at, bi, "nextindex :"+str(i), numMol
        if first <= numMol and numMol <= last :
            #print "mol index "+str(numMol)+ " : "+ name 
            lig = {"name":name.strip(), "atoms":at, "bindings":bi, "lines":(lineIndex,lineIndex+i)}
            ligands.append(lig)
        if i == -1 or numMol == last: # wrong begin line offset or end
            break
        lineIndex = lineIndex + i
        numMol += 1
    return ligands

def getLigandInfoFromJob(job, ligandfile):
    ligandsInfo = []
    
    ligandDict = {}
    worklist = []
    for runs, ligands in job.iteritems():
        workdict = {}
        ligandsMatchingRuns = []
        for l in ligands:
            ligandDict = getLigandInfo(l, l, ligandfile)[0] # returns {"name", "atoms", "bindings"i, "lines"}
            ligandDict["runs"] = runs
            ligandsInfo.append(ligandDict) # returns a list with one element so join the two element
            ligandsMatchingRuns.append(ligandDict)
        workdict["runs"] = runs
        workdict["ligands"] = ligandsMatchingRuns
        worklist.append(workdict)
        
    return ligandsInfo, worklist


# creates a file containing the ligands in ligands
def createLigandFile(filename, dir, job, ligandfile):
    workInfo = job["workinfo"]
    ligandLines = []
    file = open(ligandfile, "r")
    lines = file.readlines()
    index = 1 # indexing ligands in a file in mvd scripts start from index 1
    for work in workInfo:
        for l in work["ligands"]:
            s = l["lines"][0]
            f = l["lines"][1]

            ligandLines.extend(lines[s:f])
            l["index"] = index
            index += 1

    """
    for l in ligandsInfo:
        s = l["lines"][0]
        f = l["lines"][1]

        ligandLines.extend(lines[s:f])
"""
    path = dir+"/"+filename
    lFile = open(path,"w")
    lFile.writelines(ligandLines)
    lFile.close()
    return path 



"""
    for i in range(len(ligandStr)):
        if ligandStr[i] == beginTag:
	    molName = ligandStr[i+1]
	    molSpecs = string.split(ligandStr[i+2]," ")
	    numAtoms = molSpecs[0]
	    bindings = molSpecs[1]
	return numAtoms+bindings
"""
#ligfile = "/home/benja/molecular_docking/compounds.mol2"
"""
ligfile = "compounds.mol2"
ligandsFile = open(ligfile, "r")
ligandStr = ligandsFile.readlines()
ligandsFile.close()
#print ligandStr[4727], len(ligandStr)
(name,at,bi,index) = getNextMol(0,ligandStr)
print name, at, bi, "index :"+str(index)
while(index < len(ligandStr)):
    name,at,bi,i = getNextMol(index,ligandStr)
    #print "line"+str(index)+": ", name, at, bi, "nextindex :"+str(i)
    print name 
    if i == -1:
	break
    index = index + i
"""
#getLigandInfo2("50-140")


"""

import string
def getNextMol2(ligandsFile):
    beginTag = "@<TRIPOS>MOLECULE\r\n"
    miscLines = 9
    #print index, ligandsStrs[index]
    lines = []
    for i in range(3): 
        lines.append(ligandsFile.readline())
    #print lines
    if lines[0] != beginTag :
	print "Error : " +lines[0]
	return "empty", -1, -1,-1
    #for i in range(index,len(ligandsStrs)):
    #i = index
    if lines[0] == beginTag:
	molName = lines[1]
	molSpecs = string.split(lines[2]," ")
	#print molSpecs
	numAtoms = int(molSpecs[1])
	bindings = int(molSpecs[2])
	nextIndex = miscLines + numAtoms + bindings
        for j in range(nextIndex-3):
            ligandsFile.readline()
    return molName,numAtoms,bindings, nextIndex

def getLigandInfo(index, ligandsFile="compounds.mol2"):
    beginTag = "@<TRIPOS>MOLECULE"
    path = ""
    
    if strIndex != "" :
        hyphen = string.find(index, "-")
        if hyphen != -1:
            first = int(index[:hyphen])
            last = int(index[hyphen+1:])
        else:
            first = int(index)
            last = first
        
    ligandsFile = open(path+ligandsFile, "r")
    ligandStr = ligandsFile.readlines()
    cs = 0
    for l in ligandStr:
        cs += len(l)
    print cs, cs*32*8/1000000   
    print len(ligandStr)
    #(name,at,bi,index) = getNextMol(0,ligandStr)
    #print name, at, bi, "index :"+str(index)
    lineIndex = 0
    numMol = 0
    print first, last
    ligands = []
    while(lineIndex < len(ligandStr)):
        name,at,bi,i = getNextMol(lineIndex,ligandStr)
        #name,at,bi,i = getNextMol2(ligandsFile)
        #        print "line"+str(lineIndex)+": ", name, at, bi, "nextindex :"+str(i), numMol
        if first <= numMol and numMol <= last :
            print "mol index "+str(numMol)+ " : "+ name 
            lig = {"name":name.strip(), "atoms":at, "bindings":bi, "lines":(lineIndex,lineIndex+i)}
            ligands.append(lig)
        if i == -1 or numMol == last: # wrong begin line offset or end
            break
        lineIndex = lineIndex + i
        numMol += 1
    return ligands


def getLigandInfo2(index, ligandsFile):
    path = ""
    beginTag = "@<TRIPOS>MOLECULE"

    hyphen = string.find(index, "-")
    first = 0
    last = 0
    #print hyphen
    if hyphen != -1:
	first = int(index[:hyphen])
	last = int(index[hyphen+1:])
    else:
        first = int(index)
	last = first
    ligandsFile = open(path+ligandsFile, "r")
 
    #(name,at,bi,index) = getNextMol(0,ligandStr)
    #print name, at, bi, "index :"+str(index)
    lineIndex = 0
    numMol = 0
    #print first, last
    ligands = []
    while(1):
        #name,at,bi,i = getNextMol(lineIndex,ligandStr)
        name,at,bi,i = getNextMol2(ligandsFile)
        #        print "line"+str(lineIndex)+": ", name, at, bi, "nextindex :"+str(i), numMol
        if first <= numMol and numMol <= last :
            print "mol index "+str(numMol)+ " : "+ name 
            lig = {"name":name.strip(), "atoms":at, "bindings":bi}
            ligands.append(lig)
        if i == -1 or numMol == last: # wrong begin line offset or end
            break
        
        numMol += 1
    print ligands
    return ligands


"""
