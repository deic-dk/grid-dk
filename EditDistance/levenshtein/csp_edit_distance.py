import sys, re, time, imp, os, math, threading

(kernel,user,kernvers,t,machine) = os.uname()
if machine != "x86_64":
     imp.load_dynamic('Levenshtein', 'Levenshtein_i686.so')
else:
    if sys.maxunicode > 65535: # use different builds based on whether the host system has python unicode 2 or 4
        imp.load_dynamic('Levenshtein', 'Levenshtein_ucs4.so')
    else:
        imp.load_dynamic('Levenshtein', 'Levenshtein_ucs2.so')

from Levenshtein import distance

from process import *
from channel import *
from channelend import *

#sys.path.append("pycsp-0.6.2")

def cpu_cores():
    cpuinfo = "/proc/cpuinfo"
    f = open(cpuinfo,"r")
    lines = f.readlines()
    num_cores = " ".join(lines).count("processor")
    return num_cores

# Function for calculating the normalized edit distance.
def normalize_edit_distance( string1, string2, edit_distance ):

    # First determine the length of the longest string.
    l1 = len(string1)
    l2 = len(string2)

    max_length = float(l1);
    if l2 > l1:
        max_length = float(l2);

    # Then calculate and return the normalized edit distance.
    return "%.4f" %( 1.0 - (edit_distance / max_length) );


def read_file(inputfile):
    id_dict = {}
    ref_list = []

    f = open(inputfile, "r")
    for line in f:
        # old: Parse the line, and extract the ID and string.
        line = line.strip()
        divider = line.find(" ")
        id = line[0:divider]
        ref = line[divider+1:]
        ref = re.sub('[^a-z0-9 ]', '', ref.strip().lower(),)
        # old: Store string in dictionary (though only if it is one of the pairs we compare!).
        #ref_list = []

        if not id_dict.has_key(id):
            id_dict[id] = 1
            ref_list.append((id,ref))    
    del id_dict
    return ref_list

def edit_distance_lists(job_size, ref_list, start, out):
    num_target_refs = len(ref_list)

    if start == num_target_refs-1: # index is the last reference. We need at least one pair
        return
    
    i = start
    end_index = start+job_size
    if end_index > num_target_refs-1:
        end_index = num_target_refs-1
    
    results = []
    rescount = 0
    
    while i < end_index:
        #ref1 = ref_list[i]
        j = i+1 # we start from here
        while j < num_target_refs:
	        #ref2 = ref_list[j]
	        res = levenshtein(ref_list[i], ref_list[j])
	        #res = levenshtein(ref1, ref2)
	        
	        results.append(res)
	        rescount += 1
	        if rescount == 10000:
	            out(results)
	            #del results
	            results = []
	            rescount = 0
	        j += 1
        i += 1
    out(results)
    #del results
    
def levenshtein(ref1, ref2):
    ref1id = ref1[0] # reference id
    ref1str = ref1[1] # reference text
    ref2id = ref2[0] # reference id
    ref2str = ref2[1] # reference text
    edit_distance = distance(ref1str, ref2str)
    norm_edit_distance = normalize_edit_distance(ref1str, ref2str, edit_distance)
    #print ref1id, ref2id, edit_distance, norm_edit_distance;
    return " ".join([ref1id, ref2id, str(edit_distance), str(norm_edit_distance)])

@process
def partitioner(job_size, total_size, chan_out, workers):
    linecount = 0
    if job_size > total_size:
		job_size = total_size

    while linecount < total_size:
        chan_out((job_size, linecount))
        linecount += job_size
    
    for i in range(workers):
        chan_out((-1,-1))
    #retire(chan_out)

@process
def calculate(ref_list, chan_in, chan_out):
    while True:
	    (job_size, start_index) = chan_in()
	    if start_index == -1:
	        break
	    edit_distance_lists(job_size, ref_list, start_index, chan_out)
    chan_out([])

@process
def printer(chan_in, workers):
    remaining = workers
    while remaining > 0:
        results = chan_in()
        if results != []:
            print "\n".join(results)
        else:
            remaining -= 1
        

def edit_distance(reference_file):
    ref_list = read_file(reference_file)
    total_size = len(ref_list)
    partitioner_to_workers = Channel()
    workers_to_printer = Channel()
    #num_pairs = total_size * (total_size-1)/2
    num_workers = cpu_cores()
    
    subjob_size = int(math.ceil(float(total_size)/num_workers))
    
    Parallel(partitioner(subjob_size, total_size, OUT(partitioner_to_workers), num_workers),num_workers*calculate(ref_list, IN(partitioner_to_workers), OUT(workers_to_printer)), printer(IN(workers_to_printer), num_workers))
    
if __name__ == "__main__":
    ref_file = sys.argv[1]
    edit_distance(ref_file)
    