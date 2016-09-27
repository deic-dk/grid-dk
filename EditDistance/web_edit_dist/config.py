import os

job_summary_req = "sum"
job_status_req = "stat"
job_cancel_req = "cancel"
job_statusfile_req = "statfile"

use_remote_inputfiles = True

### Directories ###
main_app_directory = "/home/benjamin/Dokumenter/grid-dk/EditDistance"
socket_directory = "/tmp/mysockets/"
status_files_directory = "output_files/status_files/" #% main_app_directory
result_files_directory = "output_files/results/" #% main_app_directory
tmp_results_directory = "output_files/tmp_results/" #% main_app_directory
reference_files_directory = main_app_directory+"/ref_files/"
input_files_url = "https://dk.migrid.org/cert_redirect/RSLIS/nobackup/input_files/"
#input_files_url_dir = "https://dk.migrid.org/cgi-bin/fileman.py?path=RSLIS/nobackup/output_files/"
mig_RSLIS_directory = "RSLIS/nobackup/"
input_files_mig_directory = os.path.join(mig_RSLIS_directory, "input_files/")
output_files_mig_directory = os.path.join(mig_RSLIS_directory, "output_files/")

### job size ###
reference_pairs_per_job = 1000000 # 0,000025s p pair ca 
block_size = 10000 # lines       (1000 lines = 499500 pairs = ca 12,5s, 10000 l = ca 21m)
border_size = 100 # lines beyond each block will be included as border cases

### FILES###
#program_file = main_app_directory+"/levenshtein/edit_dist_grid.py"
main_edit_dist_program = main_app_directory+"/levenshtein/edit_distance.py"
edit_dist_program_files = [main_app_directory+"/levenshtein/calculate_edit_dist_seq.py", main_app_directory+"/levenshtein/csp_edit_distance.py"]
shared_lib1 = main_app_directory+"/levenshtein/Levenshtein_ucs2.so"
shared_lib2 = main_app_directory+"/levenshtein/Levenshtein_ucs4.so"
shared_lib3 = main_app_directory+"/levenshtein/Levenshtein_i686.so"
pairs_file = "pairs.pkl"
#csp_dir = main_app_directory+"/levenshtein/pycsp-0.6.2/pycsp/processes"
csp_files = ["process.py", "channel.py", "channelend.py",  "mem.py", "configuration.py"]
csp_files = [os.path.join(main_app_directory+"/levenshtein/", x) for x in csp_files]
log_file = "grid_edit_distance.log"

### MiG resource specifications ###
resource_specs = {}
resource_specs["ARCHITECTURE"]="AMD64"
#resource_specs["SANDBOX"]="1"
resource_specs["RUNTIMEENVIRONMENT"] = "PYTHON-2"
resource_specs["CPUTIME"] = 60*60*5 # 5 hours cputime
#resource_specs["DISK"] = 3 # 10000 refs produce around 2.7 GB
resource_specs["MEMORY"] = 2000
resource_specs["VGRID"] = "DCSC"
back_end_script = "ref_backend_script.py"
grid_edit_dist_script = 'grid_edit_distance.py'

### SYS limitations ###
max_procs = 4
max_filesize = 1000000000 # bytes. 1000000000 = 1GB 
