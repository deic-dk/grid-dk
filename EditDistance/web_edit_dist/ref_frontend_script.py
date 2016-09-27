import os, time, socket, random, subprocess, sys
import config
import traceback
import pickle

back_end = config.back_end_script

def running_procs():
    ps = subprocess.Popen(['ps', 'aux'], stdout=subprocess.PIPE).communicate()[0]
    #processes = ps.split('\n')
    num_procs = ps.count(back_end)
    return num_procs

def start_proc(name, ref_file, output_file):
    ed_procs = running_procs()
    if ed_procs >= config.max_procs:
        out = "%s edit distance processes are already running. Either wait until they finish or cancel some of the running processes." % ed_procs
        return out
    grid_edit_dist = "grid_edit_distance.py"
    num = random.randint(0,int(time.time()*100))
    socketname = name+"_socket"# unix socket name
    sockets_dir = config.socket_directory
    socket_path = os.path.join(sockets_dir, socketname)
    
    if not os.path.exists(sockets_dir):
        os.mkdir(sockets_dir)
        
    out = "Started edit distance process"
    priority = '-19' # nice value
    
    try:
        proc = subprocess.Popen(["nice", priority, 'python', back_end, name, socket_path, grid_edit_dist, ref_file, output_file], 
                                shell=False,
                                stdout=subprocess.PIPE) 
        
    except: 
        out = "Error starting process: \n "+traceback.format_exc()
        
    return out 

def communicate_with_proc(socketname, mess):
    ser_output = None
     
    frontend_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    frontend_socket.settimeout(5.0)
    frontend_socket.connect(socketname)
    frontend_socket.send(mess)
    ser_output = frontend_socket.recv(1024)
    frontend_socket.close()
    
    
    output_obj = pickle.loads(ser_output)
    return 1, output_obj
   
  
if __name__=="__main__":
    
    if "-u" in sys.argv:
        sock = sys.argv[sys.argv.index("-u")+1]
        mess =  sys.argv[sys.argv.index("-u")+2]
        out = communicate_with_proc(sock,mess)
        print out
    else:    
        proc_name = sys.argv[1]
        refs = sys.argv[2]
        output = sys.argv[3]
        out= start_proc(proc_name, refs, output)
        print out
