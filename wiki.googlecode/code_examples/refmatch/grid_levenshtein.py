import miglib

def create_mrsl_file(name, input_file):
 
    output_file = input_file.strip(".txt")+"_output.txt" # remove the suffix and add "_output.txt" instead
    # Notice that we don't request a Python runtime environment and use python, not $PYTHON.
    # This is in principle bad practise, but unfortunately, using shared libraries seems only to work with
    # the system's Python. So, we just hope all resources have Python installed.
    mrsl_text = """
::EXECUTE::
python levenshtein.py %s > %s

::INPUTFILES::
%s
Levenshtein_ucs4.so
Levenshtein_ucs2.so
Levenshtein_i686.so
Levenshtein_x86_64.so
levenshtein.py

::OUTPUTFILES::
%s
 
::JOBTYPE::
arc

::VGRID::
DCSC
  
""" % (input_file, output_file, input_file, output_file)

    new_file = open(name,"w")
    new_file.write(mrsl_text)
    new_file.close()
 
# the reference blocks. One for each job we want to run.
reference_files = ["block1.txt", "block2.txt", "block3.txt", "block4.txt", "block5.txt"] 

# These are static input files for each job, so we upload to the server in advance.
input_files = ["Levenshtein_ucs4.so", "Levenshtein_ucs2.so", "levenshtein.py", "Levenshtein_i686.so", "Levenshtein_x86_64.so"]

# upload each input file to the root of our home directory on the grid.dk server
for f in input_files:
    miglib.put_file(src_path=f, dst_path=f, submit_mrsl=False, extract_package=False) 
    
# Now we start a grid job for each block file
for block_file in reference_files:
    mrsl_filename = block_file.strip(".txt") + ".mRSL" # the name of the mrsl file is just block file name with .txt replaced by .mRSL. Ex.: block1.mRSL
    create_mrsl_file(name=mrsl_filename, input_file=block_file)  # create an mrsl file 
    print "Submitting "+mrsl_filename
    # upload the block file to our home directory
    miglib.put_file(src_path=block_file, dst_path=block_file, submit_mrsl=False, extract_package=False)
    # submit the job
    exit_code, out = miglib.submit_file(src_path=mrsl_filename, dst_path=mrsl_filename, submit_mrsl=True, extract_package=False) 
    print out

