
import cPickle
import imp

#sys.path.append("python-Levenshtein-0.10.1/build/lib.linux-x86_64-2.6")
#print imp.find_module("Levenshstein","Levenshtein_ucs2.so")




import sys, os

(kernel,user,kernvers,t,machine) = os.uname()
if machine != "x86_64":
     imp.load_dynamic('Levenshtein', 'Levenshtein_i686.so')
else:
    if sys.maxunicode > 65535: # use different builds based on whether the host system has python unicode 2 or 4 
        imp.load_dynamic('Levenshtein', 'Levenshtein_ucs4.so')
    else:
        imp.load_dynamic('Levenshtein', 'Levenshtein_ucs2.so')

from Levenshtein import distance

def main():
    if len(sys.argv) == 2:
        jobfilename = sys.argv[1]
    else:
        print "only takes one arg"
        sys.exit()
    job_file = open(jobfilename) 
    job_dict = cPickle.load(job_file)
    job_file.close()
    job = job_dict["pair_list"]
    submit(job)


# Function for calculating the normalized edit distance.
def normalize_edit_distance( string1, string2, edit_distance ):
    
    # First determine the length of the longest string. 
    max_length = float(len(string1));
    if len(string2) > len(string1):
        max_length = float(len(string2));
        
    # Then calculate and return the normalized edit distance.
    return "%.4f" % ( 1.0 - (edit_distance / max_length) );


def submit(job):
    for pair in job: # list of pairs
        ref1 = pair[0] # first reference (id, text) in pair
        ref2 = pair[1] # second reference (id, text) in pair
        ref1id = ref1[0] # reference id
        ref1str = ref1[1] # reference text
        ref2id = ref2[0] # reference id
        ref2str = ref2[1] # reference text
    #ref2id, ref2str =  ref1[0], ref2[1]
        #print job
        edit_distance = distance(ref1str, ref2str)
        norm_edit_distance = normalize_edit_distance(ref1str, ref2str, edit_distance)
        print ref1id, ref2id, edit_distance, norm_edit_distance;

if __name__ == "__main__":
    main()
