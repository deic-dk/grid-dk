import miglib
 
def create_mrsl_file(name, input_file):
 
    output_archivename = input_file.rstrip(".mvdscript") + "_output.tar"
    mrsl_text = \
"""::EXECUTE::
$MVD %s -nogui -licensedir .
tar -cf %s *.*

::INPUTFILES::
comodo.license
target.mvdml
compounds.mol2
%s

::OUTPUTFILES::
%s

::RUNTIMEENVIRONMENT::
MOLEGRO-VIRTUAL-DOCKER
 
::VGRID::
DCSC

::JOBTYPE::
arc
  
""" % (input_file, output_archivename, input_file, output_archivename)

    new_file = open(name,"w")
    new_file.write(mrsl_text)
    new_file.close()

# the mvd scripts detailing which molecules handle. One for each job we want to run.
script_files = ["script1.mvdscript", "script2.mvdscript"] 

# These are static input files for each job, so we upload to the server in advance.
input_files = ["target.mvdml", "compounds.mol2"]

# upload each input file to the root of our home directory on the grid.dk server
for f in input_files:
    miglib.put_file(src_path=f, dst_path=f, submit_mrsl=False, extract_package=False)
    
# Start a grid job for each .mvdscript file
for script in script_files:
    mrsl_filename = script.rstrip(".mvdscript") + ".mRSL" # the name of the mrsl file is script filename with the ".mvdscript" suffix replaced by ".mRSL".
    create_mrsl_file(name=mrsl_filename, input_file=script)  # create an mrsl file 
    miglib.put_file(src_path=script, dst_path=script, submit_mrsl=False, extract_package=False) # upload the file to our home directory
    exit_code, out = miglib.submit_file(src_path=mrsl_filename, dst_path=mrsl_filename, submit_mrsl=True, extract_package=False) #  # submit the job
    print out
