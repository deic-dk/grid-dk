#!/usr/bin/python

import cPickle, pickle, sys, re, time, os, tarfile
sys.path.append("../Gridinterface")
from gridjob import Gridjob
from gridmonitor import Gridmonitor

from gridjob_submitter import Jobsubmitter
import miginterface as mig

from timestamp import generate_timestamp
import handle_output as handle_output
import threading
import math
sys.path.append("../configuration")
import config
import urllib

class grid_edit_distance ( threading.Thread ) :
    
    def __init__(self, proc_name, input_file,result_file, status_file, mysocket, jobsize=config.reference_pairs_per_job, localmode=False):
        
        self.proc_name = proc_name
        self.input_file = input_file
        self.main_result_file = result_file 
        self.localmode = localmode
        self.status_file = status_file
        self.merged_files = []
        self.begin_time = ""
        self.end_time = ""
        self.job_manager = Gridmonitor(logfile=config.log_file)
        self.job_submitter = Jobsubmitter(logfile=config.log_file)
        self.current_state = "preparing"
        self.mysocket = mysocket
        self.job_inputfiles = [ config.shared_lib1, config.shared_lib2, config.shared_lib3]
        self.result_files = []
        self.job_size = jobsize
        self.output_directory = proc_name
        
        
        threading.Thread.__init__ ( self )
        

    """
    Creates a list job in form (ref1,ref2) where a ref is a tuple of (id,refstring)
    """
    def create_jobs_by_blocking(self,inputfile):
        
        t0_read = time.time()
        id_dict = {}
        #id_array = []
        ref_list = []
        f = open(inputfile)
        #forstart = 
        for line in f:

            # old: Parse the line, and extract the ID and string.
            #line = line.strip()
            divider = line.find(" ")
            id = line[0:divider]
            ref = line[divider+1:]
            # we don't want to filter the string here.
            #ref = re.sub('[^a-z0-9 ]', '', ref.strip().lower(),) 
            # old: Store string in dictionary (though only if it is one of the pairs we compare!).
            #ref_list = []

            #if id not in id_array: # b: only used for removing duplicates i think 
            #    id_array.append(id)
            #    ref_list.append((id,ref))      
            if not id_dict.has_key(id):
                id_dict[id] = 1
                ref_list.append((id,ref))
                
        f.close()
        print "read time %f" % (time.time()-t0_read)

        total_lines = len(ref_list)
        print total_lines
        
        ref_list.sort(key=lambda x : x[1]) # sort alphabetically 
        
        #job_size = self.job_size # config.reference_pairs_per_job
        block_size = config.block_size
        if total_lines < block_size:
            block_size = total_lines
                 
        num_blocks = int(math.ceil(float(total_lines) / float(block_size)))
        #remaining_lines = total_lines % block_size
        line_num = 0
        start_line = 0
        start_line_with_border = 0
			
        #end_line = block_size

        #job_num = 0
        result_id = self.proc_name+"__"+generate_timestamp()
        output_file_str = config.tmp_results_directory+result_id+"_%s"+".txt"
        border = config.border_size
        for bl in xrange(num_blocks):
            end_line = start_line+block_size
            block_id = "block_%i-%i" % (start_line, end_line)
            #block_filename = os.path.join(config.tmp_files,block_id+".txt")
            block_filename = block_id+".txt"
            output_filename = output_file_str % block_id
            end_line_with_border = end_line+border # python does not mind if sublist indexing exceeds last element
            block = map(lambda x : "%s %s" %(x[0],x[1]), ref_list[start_line_with_border:end_line_with_border]) # format : "<id> <refstr>" # we need to test the border cases as well
            
            block_file = open(block_filename, "w")
            for line in block:
                block_file.write(line)
                #block_file.write("\n")
            block_file.close()
            print "create time %f" % (time.time()-t0_read)
            self.deploy_block(block_filename, output_filename, config.tmp_results_directory, local=self.localmode)
            os.remove(block_filename) # clean up
            start_line = end_line
            start_line_with_border = start_line-border
            self.dump_status_file()

    def deploy_block(self, block_filename, output_file, resultdir, local):
        t0_input = time.time()
                
        inputfiles = []
        inputfiles.extend(self.job_inputfiles)
        inputfiles.append(block_filename)
        inputfiles.append(config.main_edit_dist_program)
        inputfiles.extend(config.edit_dist_program_files)
        inputfiles.extend(config.csp_files)
        output_file = output_file + " " + os.path.join(config.output_files_mig_directory, self.output_directory, os.path.basename(output_file))
        
        cmd1 = "mkdir -p %s" %resultdir
        cmd2 = "$PYTHON %s %s > %s" % (os.path.basename(config.main_edit_dist_program),block_filename, output_file)
        
        self.result_files.append(output_file)
        print self.job_inputfiles
        
        gridjob = Gridjob(commands=[cmd1, cmd2], input_files = inputfiles, output_files = [output_file], local=local, specs=config.resource_specs)
        self.job_submitter.new_job(gridjob)
        self.job_manager.add_job(gridjob)
        
        print "deploy block : "+str(time.time()-t0_input)
        return gridjob 

    def gather_output(self):
        for j in self.job_manager.jobs:
            if j.output_ready:
                out_file = j.output_files[0].split()[-1]  # note there is only one output file. It is placed after the last space in the string
                if not out_file in self.merged_files: 
                    handle_output.add_to_resultfile_compr(out_file, self.main_result_file)
                    os.remove(out_file) # remove the block result
                    self.merged_files.append(out_file)

    def dump_status_file(self):
        statusfile = open(self.status_file, "w")
        jobs = self.job_manager.jobs
        job_list = []

        for j in jobs:
            job_list.append(j.toDict())
        #job_list = jobs
        proc_status = self.create_proc_dict(job_list)
        
        pickle.dump(proc_status, statusfile)
        statusfile.close()
        
    def create_proc_dict(self, jobs):
        proc_info = {}
        proc_info["name"] = self.proc_name
        proc_info["started"] = self.begin_time
        proc_info["input"] = self.input_file
        proc_info["finished"] = self.is_done()
        proc_info["ended"] = self.end_time
        proc_info["output_dir"] = self.output_directory
        proc_info["jobs"] = jobs
        proc_info["location"] = self.status_file
        proc_info["state"] = self.current_state
        proc_info["socket_file"] = self.mysocket

        return proc_info

    def monitor_status(self):
        
        self.job_manager.update()
        
        if self.is_done():
            self.current_state = "finished"
            self.end_time = time.strftime("%X %x")
        self.dump_status_file()
            #self.gather_output()
            #if not self.job_manager.isAlive(): # exit if the job_manager thread has terminated
            #    break
            #time.sleep(10)

    def prepare_dirs(self):
        
        if not os.path.exists(config.tmp_results_directory):
            os.makedirs(config.tmp_results_directory)
    
        if not os.path.exists(config.status_files_directory):
            os.makedirs(config.status_files_directory)

        if not os.path.exists(config.result_files_directory):
            os.makedirs(config.result_files_directory)


    def merge_output(self):
        handle_output.merge_files(self.result_files,self.main_result_file)

    def is_done(self):
        if self.job_manager.jobs != []:
            return self.job_manager.all_finished()
        return False

    def cancel(self):
        self.job_submitter.cancel()
        self.job_manager.cancel_jobs()
        self.current_state = "cancelled"
        self.dump_status_file()

    def run(self):
        self.begin_time = time.strftime("%X %x")
        self.dump_status_file()
        self.prepare_dirs()
    
        self.job_submitter.start()
        #self.job_manager.start() # start jobs and start monitoring in new thread 
        
        if config.use_remote_inputfiles:
            local_path = os.path.join("/tmp/", os.path.basename(self.input_file))
            #mig_path = os.path.join(config. , "")
            self.current_state = "downloading"
            self.input_file = mig.get_output(self.input_file, local_path) # self.inputfile is already the absolute path from mig user dir
            #self.input_file = os.path.join(tmp_dir, "") 

        self.create_jobs_by_blocking(self.input_file)
        os.remove(self.input_file) # remove the local file again since we're done
        
        self.job_submitter.exit() # to ensure that the job_submitter will not exit before all jobs have been created
        #self.job_manager.done_submitting()
        
        self.current_state = "running"
                
        #self.monitor_status()
        #targz_file = handle_output.compress_file(self.main_result_file)
        #os.remove(self.main_result_file)
        #self.main_result_file = targz_file
        #self.end_time = time.strftime("%X %x")
        #if self.is_done():
        #    self.current_state = "finished"
        
        while self.job_submitter.isAlive():
            time.sleep(10)
            self.dump_status_file()
        
        
        
        print "grid edistance thread exiting"

if __name__=="__main__":
    runlocal = False
    if "-l" in sys.argv:
        runlocal = True
    if len(sys.argv) == 1:
        print "Usage: input file needed."
        sys.exit()


    inputfile = sys.argv[1]

    result_file = sys.argv[2]
    js = config.reference_pairs_per_job
    if "-js" in sys.argv:
        i = sys.argv.index("-js")
        js = int(sys.argv[i+1])


    name = "standalone_test"
    status_file = name+"_status.pkl"
    socket = name + "_socket"

    edit_dist = grid_edit_distance(name, inputfile,result_file, status_file, socket, jobsize=js, localmode=False)
    edit_dist.start()
    edit_dist.join()
    
    
