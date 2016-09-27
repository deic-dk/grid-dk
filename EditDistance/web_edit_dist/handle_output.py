import os, tarfile, shutil
def merge_files(files, resultfilename):
    #mergefile = resultfilename
    #os.remove(mergefile)
    #print os.listdir(".")
    concat_file = open(resultfilename,"w")
    #files = os.listdir(folder)
    
    for f in files:
        resfile = open(f,"r") 
        lines= resfile.readlines()
        concat_file.writelines(lines)
        resfile.close()
    
    concat_file.close()

def add_to_resultfile(output_filename, result_filename):
    
    #mergefile = resultfilename
    #os.remove(mergefile)
    #print os.listdir(".")
    result_file = open(result_filename,"a")
    #files = os.listdir(folder)
    
    output_file = open(output_filename,"r") 
    
    for line in output_file:
        result_file.write(line)

    #lines = output_file.readlines()
    #result_file.writelines(lines)
    output_file.close()
    result_file.close()


def add_to_resultfile2(output_filename, result_filename):
    
    #mergefile = resultfilename
    #os.remove(mergefile)
    #print os.listdir(".")
    result_file = open(result_filename,"wb")
    #files = os.listdir(folder)
    
    output_file = open(output_filename,"r") 
    
    #destination = open(outfile,'wb')
    shutil.copyfileobj(output_file, destination)
    #shutil.copyfileobj(open(file2,'rb'), destination)
    #destination.close()
    #lines = output_file.readlines()
    #result_file.writelines(lines)
    output_file.close()
    result_file.close()



def add_to_resultfile_compr(output_filename, result_filename):
    
    #mergefile = resultfilename
    #os.remove(mergefile)
    #print os.listdir(".")
    
    tar_filepath = result_filename
    #tar_obj = open(tar_filepath, "w")
    if os.path.exists(tar_filepath):
        tar = tarfile.open(tar_filepath,mode="a")
    else:
	    tar = tarfile.open(tar_filepath,mode="w")
    #output_file = open(output_filename,"r")
    
    #for line in output_file:
    tar.add(output_filename, os.path.basename(output_filename))
    tar.close()
    
    #result_file = open(result_filename,"a")
    #files = os.listdir(folder)

    #output_file.close()
    #tar.close()

def compress_file(file_path):
	dir_name, file_name = os.path.split(file_path)
	tar_filepath = os.path.join(dir_name,file_name+".tar.gz")
	tar = tarfile.open(tar_filepath,"w:gz")
	tar.add(file_path, file_name) 
	tar.close()
	return tar_filepath

def merge_output(folder):
    
    mergefile = "merged_file.txt"
    #os.remove(mergefile)
    concat_file = open(folder+"merged_file.txt","w")
    files = os.listdir(folder)
    
    for f in files:
        resfile = open(folder+f,"r") 
        lines= resfile.readlines()
        concat_file.writelines(lines)
        resfile.close()
    concat_file.close()

if __name__=="__main__":
    output_filename = "output_files/results/result_160341_2_3_2010"
    result_filename = "my.tar"
    add_to_resultfile_compr(output_filename, result_filename)
    

