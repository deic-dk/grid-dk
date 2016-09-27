import os
import signal
import time
import sys
import imp
import socket
import config
import pickle
import threading


###### signal handlers#########

class handle_request_thread(threading.Thread):
    def __init__(self, connection):
        self.connection = connection
        threading.Thread.__init__ ( self )
        
    def run(self):
        try:
            received_req = self.connection.recv(1024) # wait for status req
            
            print received_req
            reply = handle_request(received_req)
            print reply
            serialized_obj = pickle.dumps(reply)
            self.connection.send(serialized_obj) # send to front end
            self.connection.close()
        except socket.error, msg:
            print msg

"""
Determines how to handle the request messages from the frontend process. Return the string to reply.
"""
def handle_request(req):
    if req.strip() == config.job_summary_req:
        "return a jobname, inputfile, outputfilename, time, overallstatus, cancel"
        #if edit_dist.current_state == "preparing":
        done = edit_dist.is_done()
        summary_obj = create_summary_dict(done)
        return summary_obj

    if req.strip() == config.job_statusfile_req:
        return status_file
       
    if req.strip() == config.job_status_req:
        if edit_dist.current_state == "preparing":
            return "Creating jobs"

        status_list = edit_dist.job_manager.jobs
        return status_list 

    if req.strip() == config.job_cancel_req:
        edit_dist.cancel()
        return "Process cancelled"
        #sys.exit()

def main():
    edit_dist.start()  # start edit distance thread
    backend_socket.settimeout(10.0)
    while edit_dist.isAlive():
        try: 
            
            (socket_to_frontend,_)  = backend_socket.accept()
            handle_request_thread(socket_to_frontend).run()

        except socket.timeout, msg:
            #print "backend socket time outcheck"
            continue
        except socket.error, msg:
            print msg
        except KeyboardInterrupt:
            print "keyboard interrupt. Exiting..."
            break

    backend_socket.close()
    os.remove(socket_file) # cleanup: remove the socket
        
def create_summary_dict(done):
    job_summary = {}
    job_summary["name"] = proc_name
    job_summary["started"] = begin_time
    job_summary["input"] = inputfile
    job_summary["finished"] = done
    job_summary["ended"] = end_time
    job_summary["output"] = resultfile
    return job_summary
    
if __name__=="__main__":
    f = open(config.log_file, "a")
    sys.stdout = f
    sys.stderr = f
    print "backend started"
    proc_name = sys.argv[1]# human readable identifier for this process
    socket_file = sys.argv[2]

    if not os.path.exists(config.socket_directory):
        os.mkdir(config.socket_directory)

    py_file = sys.argv[3]
    
    daemon = imp.load_source("daemon", py_file)
    
    inputfile = sys.argv[4]#"mini_reference-strings.txt"
    resultfile = sys.argv[5]#"result.txt" 

    if os.path.exists(proc_name):
        proc_name += proc_name+timestamp
        
    status_file = os.path.join(config.status_files_directory, proc_name + ".pkl")
    resultfile = os.path.join(config.result_files_directory, resultfile)
    
    timestamp = str(int(time.time()*100))

    if os.path.exists(resultfile):
        resultfile += timestamp
    
    edit_dist = daemon.grid_edit_distance(proc_name, inputfile, resultfile, status_file, socket_file, localmode=0)
    backend_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    backend_socket.bind(socket_file)
    backend_socket.listen(5) # number of queued connections
  
    begin_time = time.strftime("%X %x")
    end_time = ""
    print "starting edit dist"
    
    main()  
