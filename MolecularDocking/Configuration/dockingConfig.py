
# dirs
dockworkingDir = "Dock_working_dir/"
mvdProgram = "Molegro/MVD/bin/mvd"
#resultDirectory = dockworkingDir+"dockingresults/"
resultDirectory = "dockingresults/"
dockingscriptsDir = dockworkingDir+"createscript/"
moleculesDir = dockingscriptsDir#dockworkingDir[:-1] #"molecules"
dockingResultsFilename = "DockingResults_main.mvdresults"

# log
logfile = "dockingLog.txt"
#mvdLogFile = "MVDScriptLog_main.txt"

# mvd input files if installed locallly. Location needs to be subdir of the grid docker home dir.
MvdInputFiles = [
"Molegro/MVD/misc/data/ElementTable.csv",
"Molegro/MVD/misc/data/PreparationTemplate.xml",
"Molegro/MVD/misc/data/Residues.txt",
"Molegro/MVD/misc/data/RerankingCoefficients.txt",
"Molegro/MVD/misc/data/sp3sp3a.csv",
"Molegro/MVD/misc/data/sp2sp2a.csv",
"Molegro/MVD/misc/data/sp2sp3a.csv",
"Molegro/MVD/misc/data/BindingAffinity.mdm",
"Molegro/MVD/bin/comodo.license", 
"Molegro/MVD/bin/mvd"]

server_files = ["DCSC/comodo.license"] # these need to be uploaded but must appear in the submit grid script

license = "Molegro/MVD/bin/comodo.license"

ligandfilesPrefix = "ligands"
outputfilesPrefix = "dock"

pollFrequency = 10
fragmentStrategy = "ligands" # "ligands" for ligand-based or "runs" for run-based fragmentation
 
######### Grid script specifications: contents of the mRSL file ################

use_mvd_RTE = True
RTE_bin = "$MVD"
MiG_resource_specs = {}
MiG_resource_specs = {"VGRID":"DCSC"} # field:value (as strings)
#MiG_resource_specs["ARCHITECTURE"] ="AMD64"

#MiG_resource_specs["ARCHITECTURE"] ="X86" # on portal.grid.dk it does not work on mig resource

MiG_resource_specs["RUNTIMEENVIRONMENT"] ="MOLEGRO-1.0"
MiG_resource_specs["ENVIRONMENT"] ="MVD_LICENSE=DCSC/comodo.license"


######## Docking specifications  ############

protein_file = "molecules/target.mvdml"
#ligands_file  ="molecules/compounds.mol2"
ligands_file  ="molecules/test_ligands.mol2"
num_ligands = 7 # ligands in test_ligands.mol2"

runs = 1  # how many runs per ligand. Results can vary from run to run. 
jobsize = 4 #  one job unit consists of 1 ligand, run 1 time. Ex.: 2 ligands docked, run twice creates 4 units.
