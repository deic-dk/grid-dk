import miglib
import pickle
 
def create_mrsl_file(name, input_file, output_file):
 
    mrsl_text = \
"""::EXECUTE::
$PYTHON epistasis.py %s

::INPUTFILES::
EpiMain.R
EpiCRnew_R_edit.R
EpiLW.R
DistrPost07_R_edit.R
epistasis.py
SkizoGWA1.sav
%s

::RUNTIMEENVIRONMENT::
PYTHON-2.7
R-2.13.1

::OUTPUTFILES::
%s

::VGRID::
DCSC

::JOBTYPE::
arc

""" % (input_file, input_file, output_file)

    new_file = open(name,"w")
    new_file.write(mrsl_text)
    new_file.close()

def create_job_file(filename, class_value, output_file):

    gene_indexes = range(5,10,1)
    trait_indexes = range(3,5,1)
    
    job_file = {}
    job_file['data_file'] = "SkizoGWA1.sav"
    job_file['class'] = class_value
    job_file['selection_variable'] = 2 # index
    job_file['output_dir'] = "epistasis_files/"
    job_file['gene_list'] = gene_indexes
    job_file['trait_list'] = trait_indexes
    job_file["r_files"] = ["EpiCRnew_R_edit.R","DistrPost07_R_edit.R","EpiLW.R"]
    job_file["main_r_file"] = "EpiMain.R"
    job_file["r_bin"] = "$R" 
    job_file['output_files'] = [output_file]
    f = open(filename, "w")
    pickle.dump(job_file, f)
    f.close()
# These are static input files for each job, so we upload to the server in advance.
input_files = ["EpiMain.R", "EpiCRnew_R_edit.R", "EpiLW.R", "DistrPost07_R_edit.R", "epistasis.py", "SkizoGWA1.sav"]

# upload each input file to the root of our home directory on the grid.dk server
for f in input_files:
    miglib.put_file(src_path=f, dst_path=f, submit_mrsl=False, extract_package=False)
    
classes = [1,2]
# Start a grid job for each .mvdscript file
for c in classes:
    job_filename = "epistasis_job"+str(c)+ ".pkl" # the name of the mrsl file is script filename with the ".mvdscript" suffix replaced by ".mRSL".
    mrsl_filename = "epistasis_job"+str(c)+".mRSL" # the name of the mrsl file is script filename with the ".mvdscript" suffix replaced by ".mRSL".
    output_filename = 'epistasis_files' + str(c) + '.tar.gz'
    create_job_file(job_filename, c, output_filename)
    create_mrsl_file(name=mrsl_filename, input_file=job_filename, output_file=output_filename)  # create an mrsl file 
  
    #import subprocess
    #cmd = "python epistasis.py "+job_filename
    #proc = subprocess.Popen(cmd, shell=True)
    #proc.wait()
    print "Submitting "+mrsl_filename
    # upload the block file to our home directory
    miglib.put_file(src_path=job_filename, dst_path=job_filename, submit_mrsl=False, extract_package=False)
    # submit the job
    exit_code, out = miglib.submit_file(src_path=mrsl_filename, dst_path=mrsl_filename, submit_mrsl=True, extract_package=False)
    print out
