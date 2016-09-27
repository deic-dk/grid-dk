import shutil
import os
import time
import tarfile
import createmrsl
import sys 
#sys.path.append("Gridinterface/migscripts/")
#import miglib
import miglib as miglib
import string 

from mylogger import log

####### CREATE JOBS / SUBMIT ############
"""
creates an mrsl file with to submit the job. All files in input_files that are not in cached_files will be upload.
"""
def create_job(exec_commands, input_files, executables, local_working_dir, mig_working_dir, output_files, cached_files=[], resource_specs={}, args=[], name=""):

    #job_files = [] 
    #job_files.extend(input_files)

    #if static_files != []:
     #   job_files.extend(static_files)
        
    
   #copy_files_to_working_dir(job_files, local_working_dir)
   # if args !=[]:
   #     arg_files = write_args_to_files(args, local_working_dir)
    #    files_to_upload.extend(arg_files)
    
    #expected_output = [mig_working_dir+output_files[0]]
        
    # make MRSL
    if name == "":
        timestamp = str(int(time.time()*100))
        name = "submit_file_"+timestamp
    mrsl_filename = name+".mRSL"
        
    mrsl_path = local_working_dir+mrsl_filename
    mrsl_file = createmrsl.generate_mrsl(mrsl_path, exec_commands, input_files, output_files, local_working_dir, executables, resource_specs_dict=resource_specs)
    
    files_to_upload = []

    files_to_upload.append(mrsl_file)
    for f in input_files:
        if not f in cached_files:
            files_to_upload.append(f)

    #timestamp = str(int(time.time()*100))
    tar_name = "inputfiles"+name+".tar.gz"
    archive = create_archive(tar_name, files_to_upload, local_working_dir, mig_working_dir, keepSubFolders=True)  # local_working_dir  ==  mig_working_dir at the moment
    #(code, out) = miglib.submit_file(mrslfile,local_working_dir,True,False)
    #out = mig_function_wrapper(miglib.submit_file,mrslfile,local_working_dir,True,False)
    mig_archive_dest = archive.split("/")[-1]

    makeFolderTree(files_to_upload)

    out = mig_function_wrapper(miglib.submit_file,archive,mig_archive_dest,True,True) # upload job archive and submit mrsl
       
    job_id = out[-1].split("'")[-2]
    #clean_up_locally([mrsl_file]) # delete generated mrsl file
    #cleanUpInputFiles(files_to_upload) # delete job input files 
    remove_files([mig_archive_dest, mrsl_file])
    #remove_files_local(files_to_upload)
    remove_files_local([archive, mrsl_file])
    
    return job_id


def prepare_job(exec_commands, input_files, executables, local_working_dir, mig_working_dir, output_files, static_files=[], vgrid="Generic", resource_specs={}, args=[]):
    job_files = [] 
    job_files.extend(input_files)
    if static_files != []:
        job_files.extend(static_files)
    
    files_to_upload = copy_files_to_working_dir(job_files, local_working_dir)
    if args !=[]:
        arg_files = write_args_to_files(args, local_working_dir)
        files_to_upload.extend(arg_files)

    expected_output = [mig_working_dir+output_files[0]]
    # make MRSL
    mrsl_file = createmrsl.generate_mrsl(exec_commands, files_to_upload, expected_output, local_working_dir, executables, resource_specs_dict=resource_specs)
    files_to_upload.append(mrsl_file)
        
    return mrsl_file


def submit_job(job_file, dest_dir):
    #print job_file
    out = mig_function_wrapper(miglib.submit_file,job_file,dest_dir,True,False) 
#out = mig_function_wrapper(miglib.submit_file,mrslfile,local_working_dir,True,False)
#(code, out) = miglib.submit_file(mrslfile,local_working_dir,True,False)
    #print out
    #exit(0)
    job_id = out[-1].split(" ")[0]
    
#print
#append
    return job_id


def write_args_to_files(args, dest_dir):
    import pickle
    num = 0
    arg_files = []
    for arg in args:
        fname = dest_dir+"arg"+str(num)+".pkl"
        output = open(fname, 'w')
        pickle.dump(arg, output)
        output.close()
        arg_files.append(fname)
        num +=1
    return arg_files


def copy_files_to_working_dir(input_files, dest_dir):
    files = []
    for f in input_files: 
        cp_filename = dest_dir+f.split("/")[-1]
        shutil.copyfile(f ,cp_filename)
        files.append(cp_filename)
        
    return files    
   

def create_archive(tar_name, input_files, temp_dir, remote_dir, keepSubFolders=False):
        #ScriptsWrapper.makeDir(remoteDir, recursive=True)
    #makeDirTree(remoteDir)
    tar_path = temp_dir+tar_name
    tar = tarfile.open(tar_path,"w:gz")
    
    for f in input_files:
        if not keepSubFolders:
            filename = f.split("/")[-1]
        else:
            tar.add(f, f) 
    tar.close()

    return tar_path# delete the tar file in the mig server when it has been extracted


def upload_file(local_filename, remote_filename):
    submit = False
    extract = False
    output = mig_function_wrapper(miglib.put_file, local_filename, remote_filename, submit, extract)
    return output

def upload_files(files, remote_dir, create_archive=False, recursive=False):
        #ScriptsWrapper.makeDir(remoteDir, recursive=True)
    #makeDirTree(remoteDir)
    #timestamp = str(time.time())
    #tarName = "inputfiles"+timestamp+".tar.gz"
    #tar_path = tempDir+tarName
    #tar = tarfile.open(tar_path,"w:gz")
    #remote_dir.strip("/")+"/"+
    if recursive:
        makeFolderTree(files)
    #for f in inputfiles:
    #    filename = f.split("/")[-1]
    #    tar.add(f, remoteDir+filename) 
    #tar.close()
    #print "uploading"
    #print input_files
    #outStrs = ScriptsWrapper.put(tarpath, tarName)
    out_list = list()
    submit = False
    if create_archive:
        
        extract = True
        archive = create_archive(files, remote_dir,remote_dir,keepSubFolders)
        mig_function_wrapper(miglib.put_file,archive, remote_dir,submit,  extract)
    else:
        extract = False
        for f in files:
            #output = mig_function_wrapper(miglib.put_file, f, remote_dir, submit, extract)
            out_list.append(upload_file(f, f))
        #archive = create_archive(files, remote_dir,remote_dir,keepSubFolders)
#     
    #if as_archive:
    

#print output
    #print "uploading done"
    #return "hej"# delete the tar file in the mig server when it has been extracted
    #ScriptsWrapper.removeFile(tarName)
    #miglib.rm_file(tarName)
    # delete the locally staged files
    #cleanUpLocally([tarpath])
    return out_list
            

def mk_dir(dirname):
    #path_str = ""
    path_str = "path="+dirname

    return mig_function_wrapper(miglib.mk_dir,path_str)
  

def ls(path):
    path_str = "path="+path
    out = mig_function_wrapper(miglib.ls_file,path_str)
    files = map(lambda x : x.strip("\t\n"), out)
    #print files
    return files 

def path_exists(path):
    output = ls(path) # either return a list of files or a list of error messages
    not_found_error = "105"
    exists = not not_found_error in "".join(output)
    
    #if not exists: # maybe path is a dir
    #    exists = files != []
    #print "output", output
    #print path, exists
    #exit(0)
    return exists
   
###### OUTPUT ##########

def get_output(mig_filelocation, local_filelocation):
    #success = ScriptsWrapper.get(filename, destinationDir)
    out = mig_function_wrapper(miglib.get_file,mig_filelocation, local_filelocation)
    #print code, out
#if success:
    #  
    #else: 
    #    print "Can't get file : "+filename
    #    return ""
    #MiG.removeFiles(filename)
    #MiG.removeDir(job["workingDir"]) # directory
    #allfiles.extend(job["outputfiles"])  # output
    return local_filelocation

####### STATUS / UPDATE ########

def get_status(job_ids):
    #statusStr = ScriptsWrapper.status(jobId)
    #print job_ids
    job_id_list = "job_id=%s" % ";job_id=".join(job_ids) # necessary format for miglib.rm_file()
    job_status_list = mig_function_wrapper(miglib.job_status,job_id_list)
    #print statusStr
    job_info = parse_job_info( job_status_list)
    #print job_info
    
    return job_info

def parse_status(status_msg):
    #import time
    status_msg_lines = status_msg.split("\n")
    job_info = {}
    for line in status_msg_lines:
        ls = line.split(": ")
        if len(ls) > 1:
            job_info[ls[0].upper()] = ls[1].strip() 
    #print jobInfo
    return job_info

def parse_job_info(status_list):
    #import time
    #print str(status_list)
    status_str = "".join(status_list)
    job_info_str_list= status_str.split("Job ")[1:] # we don't need the preceding  information
    job_info_list = []
    for ji in job_info_str_list:
        status = parse_status(ji)
        job_info_list.append(status)
    return job_info_list


####### CANCEL ################

def cancel_job(job_id):
    #out = ScriptsWrapper.cancel(jobid)
    out = mig_function_wrapper(miglib.cancel_job,job_id)
    return out 


#### CLEAN UP / DELETE ##########

def remove_files(filenames):
    files_str = ""
    path_list = "path=%s" % ";path=".join(filenames) # necessary format for miglib.rm_file()
    #for f in filenames:
    #    files_str += f + " "
        
    #return ScriptsWrapper.removeFile(filesStr)
    return mig_function_wrapper(miglib.rm_file,path_list)

#def remove_file(filename):
     #return ScriptsWrapper.removeFile(filesStr)
 #   return mig_function_wrapper(miglib.rm_file,filename)

def remove_dir(dirname):
    #return ScriptsWrapper.removeDir(dirname)
    path_list = "path=%s" % ";path=".join([dirname]) # necessary format for miglib.rm_dir()
    return mig_function_wrapper(miglib.rm_dir,path_list)


def dir_cleanup(job_files, directory):
    for f in job_files:
        filename = directory+f.split("/")[-1]
        #print "removing ", filename
        #ScriptsWrapper.removeFile(filename)
        #print out

def remove_files_local(files):
    tmp_dir = "/tmp/"
      #clean up
    for f in files:
        try: 
            #print "removing "+f+" locally"
            #os.remove(f)
            shutil.move(f,tmp_dir+f)
        except OSError:
            print "Can't delete : "+f


def mig_function_wrapper(func,*args):
    #print args
    #funct = "miglib."+func
    #print func, args
    retries = 3
    retry_wait = 2 # 2 seconds
    exit_code, out = func(*args)
    #print func, args
    #print "mig answer: ", exit_code, out
    if exit_code != 0:
        exit_code = get_exit_code(out)
    
    #print "exit code", exit_code
    if exit_code != 0:
        for i in range(retries):
            time.sleep(retry_wait)
            print out
            print "exit code", exit_code, "retrying... ",i
            code, out = func(*args)
            exit_code = get_exit_code(out)
            if exit_code == 0:
                return out
        raise Exception("MiG Error: \n"+str(func)+":"+str(args)+"\n"+"".join(out))
    else:
        return out

def command_test():
    (code, out) = miglib.ls_file(".")
    success = out != []
    return success, miglib.ls_file
    
def get_exit_code(output_lines):
    if len(output_lines) > 0:
        exit_code_str = output_lines[0]
        code = exit_code_str.strip("'Exit code: ").split()[0]
        #print code
    else:
        code = -1
        
    return int(code)

"""
Would be used to create folder tree before extracting a tar. This is necessary because the auto-extract miglib option does not create directories.
"""
def makeFolderTree(files):
    processed_paths = []
    for f in files:
        path = ""
        directory = os.path.dirname(f)
        if directory != "": # must be a dir
            subfolders = directory.split(os.sep)
            for folder in subfolders:
                path = os.path.join(path,folder)
                if not path in processed_paths:
                    processed_paths.append(path) # don't process it again
                    if not path_exists(path):
                        mk_dir(path)
                        
