import sys
version = sys.version.split()[0]
reference_file = sys.argv[1]
#print version
#if version >= "2.6":
#    from csp_edit_distance import edit_distance
#else:
from calculate_edit_dist_seq import edit_distance

edit_distance(reference_file)
